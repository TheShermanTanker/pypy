from rpython.rlib.rarithmetic import (r_uint, r_ulonglong, r_longlong,
                                      maxint, intmask)
from rpython.rlib import rutf8
from rpython.rlib.objectmodel import specialize
from rpython.rlib.rstruct.error import StructError
from rpython.rlib.rstruct.formatiterator import FormatIterator

from pypy.interpreter.error import OperationError


class PackFormatIterator(FormatIterator):
    def __init__(self, space, wbuf, args_w):
        self.space = space
        self.args_w = args_w
        self.args_index = 0
        self.pos = 0
        self.wbuf = wbuf

    def advance(self, count):
        self.pos += count

    # This *should* be always unroll safe, the only way to get here is by
    # unroll the interpret function, which means the fmt is const, and thus
    # this should be const (in theory ;)
    @specialize.arg(1)
    def operate(self, fmtdesc, repetitions):
        if fmtdesc.needcount:
            fmtdesc.pack(self, repetitions)
        else:
            for i in range(repetitions):
                fmtdesc.pack(self)
    _operate_is_specialized_ = True

    def align(self, mask):
        pad = (-self.pos) & mask
        for i in range(self.pos, self.pos+pad):
            self.wbuf.setitem(i, '\x00')
        self.advance(pad)

    def finished(self):
        if self.args_index != len(self.args_w):
            raise StructError("too many arguments for struct format")

    def accept_obj_arg(self):
        try:
            w_obj = self.args_w[self.args_index]
        except IndexError:
            raise StructError("struct format requires more arguments")
        self.args_index += 1
        return w_obj

    def accept_int_arg(self):
        return self._accept_integral("int_w")

    def accept_uint_arg(self):
        return self._accept_integral("uint_w")

    def accept_longlong_arg(self):
        return self._accept_integral("r_longlong_w")

    def accept_ulonglong_arg(self):
        return self._accept_integral("r_ulonglong_w")

    @specialize.arg(1)
    def _accept_integral(self, meth):
        space = self.space
        w_obj = self.accept_obj_arg()
        if (space.isinstance_w(w_obj, space.w_int) or
            space.isinstance_w(w_obj, space.w_long)):
            w_index = w_obj
        else:
            w_index = None
            if space.lookup(w_obj, '__index__'):
                try:
                    w_index = space.index(w_obj)
                except OperationError as e:
                    if not e.match(space, space.w_TypeError):
                        raise
                    pass
            if w_index is None and space.lookup(w_obj, '__int__'):
                if space.isinstance_w(w_obj, space.w_float):
                    msg = "integer argument expected, got float"
                else:
                    msg = "integer argument expected, got non-integer" \
                          " (implicit conversion using __int__ is deprecated)"
                space.warn(space.newtext(msg), space.w_DeprecationWarning)
                w_index = space.int(w_obj)   # wrapped float -> wrapped int or long
            if w_index is None:
                raise StructError("cannot convert argument to integer")
        method = getattr(space, meth)
        try:
            return method(w_index)
        except OperationError as e:
            if e.match(self.space, self.space.w_OverflowError):
                raise StructError("argument out of range")
            raise

    def accept_bool_arg(self):
        w_obj = self.accept_obj_arg()
        return self.space.is_true(w_obj)

    def accept_str_arg(self):
        w_obj = self.accept_obj_arg()
        return self.space.bytes_w(w_obj)

    def accept_unicode_arg(self):
        w_obj = self.accept_obj_arg()
        return self.space.utf8_len_w(w_obj)

    def accept_float_arg(self):
        w_obj = self.accept_obj_arg()
        try:
            return self.space.float_w(w_obj)
        except OperationError as e:
            if e.match(self.space, self.space.w_TypeError):
                raise StructError("required argument is not a float")
            raise


class UnpackFormatIterator(FormatIterator):
    def __init__(self, space, buf):
        self.space = space
        self.buf = buf
        self.length = buf.getlength()
        self.pos = 0
        self.result_w = []     # list of wrapped objects

    # See above comment on operate.
    @specialize.arg(1)
    def operate(self, fmtdesc, repetitions):
        if fmtdesc.needcount:
            fmtdesc.unpack(self, repetitions)
        else:
            for i in range(repetitions):
                fmtdesc.unpack(self)
    _operate_is_specialized_ = True

    def align(self, mask):
        self.pos = (self.pos + mask) & ~mask

    def finished(self):
        if self.pos != self.length:
            raise StructError("unpack str size too long for format")

    def can_advance(self, count):
        end = self.pos + count
        return end <= self.length

    def advance(self, count):
        if not self.can_advance(count):
            raise StructError("unpack str size too short for format")
        self.pos += count

    def read(self, count):
        curpos = self.pos
        self.advance(count) # raise if we are out of bound
        return self.buf.getslice(curpos, 1, count)

    @specialize.argtype(1)
    def appendobj(self, value):
        # CPython tries hard to return int objects whenever it can, but
        # space.newint returns a long if we pass a r_uint, r_ulonglong or
        # r_longlong. So, we need special care in those cases.
        is_unsigned = (isinstance(value, r_uint) or
                       isinstance(value, r_ulonglong))
        if is_unsigned:
            if value <= maxint:
                w_value = self.space.newint(intmask(value))
            else:
                w_value = self.space.newint(value)
        elif isinstance(value, r_longlong):
            if value == r_longlong(intmask(value)):
                w_value = self.space.newint(intmask(value))
            else:
                w_value = self.space.newint(value)
        elif isinstance(value, bool):
            w_value = self.space.newbool(value)
        elif isinstance(value, int):
            w_value = self.space.newint(value)
        elif isinstance(value, float):
            w_value = self.space.newfloat(value)
        elif isinstance(value, str):
            w_value = self.space.newbytes(value)
        elif isinstance(value, unicode):
            w_value = self.space.newutf8(value.decode('utf-8'), len(value))
        else:
            assert 0, "unreachable"
        self.result_w.append(w_value)

    def append_utf8(self, value):
        w_ch = self.space.newutf8(rutf8.unichr_as_utf8(r_uint(value)), 1)
        self.result_w.append(w_ch)

    def get_pos(self):
        return self.pos

    def get_buffer_and_pos(self):
        return self.buf, self.pos

    def skip(self, size):
        self.read(size) # XXX, could avoid taking the slice
