import gc
import os
import py

from rpython.rlib.rarithmetic import r_singlefloat, r_longlong, r_ulonglong
from rpython.rlib.test.test_clibffi import BaseFfiTest, make_struct_ffitype_e
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rtyper.lltypesystem.ll2ctypes import ALLOCATED
from rpython.rtyper.llinterp import LLException
from rpython.translator import cdir
from rpython.rlib.libffi import (CDLL, ArgChain, types,
                              IS_32_BIT, IS_WIN64, array_getitem, array_setitem)
from rpython.rlib.libffi import (struct_getfield_int, struct_setfield_int,
                              struct_getfield_longlong, struct_setfield_longlong,
                              struct_getfield_float, struct_setfield_float,
                              struct_getfield_singlefloat, struct_setfield_singlefloat)

class TestLibffiMisc(BaseFfiTest):

    CDLL = CDLL

    def test_argchain(self):
        chain = ArgChain()
        assert chain.numargs == 0
        chain2 = chain.arg(42)
        assert chain2 is chain
        assert chain.numargs == 1
        intarg = chain.first
        assert chain.last is intarg
        assert intarg.intval == 42
        chain.arg(123.45)
        assert chain.numargs == 2
        assert chain.first is intarg
        assert intarg.next is chain.last
        floatarg = intarg.next
        assert floatarg.floatval == 123.45

    def test_wrong_args(self):
        # so far the test passes but for the wrong reason :-), i.e. because
        # .arg() only supports integers and floats
        chain = ArgChain()
        x = lltype.malloc(lltype.GcStruct('xxx'))
        y = lltype.malloc(lltype.GcArray(rffi.SIGNED), 3)
        z = lltype.malloc(lltype.Array(rffi.SIGNED), 4, flavor='raw')
        py.test.raises(TypeError, "chain.arg(x)")
        py.test.raises(TypeError, "chain.arg(y)")
        py.test.raises(TypeError, "chain.arg(z)")
        lltype.free(z, flavor='raw')

    def test_library_open(self):
        lib = self.get_libc()
        del lib
        gc.collect()
        assert not ALLOCATED

    def test_library_get_func(self):
        lib = self.get_libc()
        ptr = lib.getpointer('fopen', [], types.void)
        py.test.raises(KeyError, lib.getpointer, 'xxxxxxxxxxxxxxx', [], types.void)
        del ptr
        del lib
        gc.collect()
        assert not ALLOCATED

    def test_struct_fields(self):
        longsize = 4 if IS_32_BIT or IS_WIN64 else 8
        POINT = lltype.Struct('POINT',
                              ('x', rffi.LONG),
                              ('y', rffi.SHORT),
                              ('z', rffi.VOIDP),
                              )
        y_ofs = longsize
        z_ofs = longsize*2
        p = lltype.malloc(POINT, flavor='raw')
        if IS_WIN64:
            p.x = rffi.cast(rffi.LONG, 42)
        else:
            p.x = 42
        p.y = rffi.cast(rffi.SHORT, -1)
        p.z = rffi.cast(rffi.VOIDP, 0x1234)
        addr = rffi.cast(rffi.VOIDP, p)
        assert struct_getfield_int(types.slong, addr, 0) == 42
        assert struct_getfield_int(types.sshort, addr, y_ofs) == -1
        assert struct_getfield_int(types.pointer, addr, z_ofs) == 0x1234
        #
        struct_setfield_int(types.slong, addr, 0, 43)
        struct_setfield_int(types.sshort, addr, y_ofs, 0x1234FFFE) # 0x1234 is masked out
        struct_setfield_int(types.pointer, addr, z_ofs, 0x4321)
        assert p.x == 43
        assert p.y == -2
        assert rffi.cast(rffi.LONG, p.z) == 0x4321
        #
        lltype.free(p, flavor='raw')

    def test_array_fields(self):
        POINT = lltype.Struct("POINT",
            ("x", lltype.Float),
            ("y", lltype.Float),
        )
        points = lltype.malloc(rffi.CArray(POINT), 2, flavor="raw")
        points[0].x = 1.0
        points[0].y = 2.0
        points[1].x = 3.0
        points[1].y = 4.0
        points = rffi.cast(rffi.CArrayPtr(lltype.Char), points)
        assert array_getitem(types.double, 16, points, 0, 0) == 1.0
        assert array_getitem(types.double, 16, points, 0, 8) == 2.0
        assert array_getitem(types.double, 16, points, 1, 0) == 3.0
        assert array_getitem(types.double, 16, points, 1, 8) == 4.0
        #
        array_setitem(types.double, 16, points, 0, 0, 10.0)
        array_setitem(types.double, 16, points, 0, 8, 20.0)
        array_setitem(types.double, 16, points, 1, 0, 30.0)
        array_setitem(types.double, 16, points, 1, 8, 40.0)
        #
        assert array_getitem(types.double, 16, points, 0, 0) == 10.0
        assert array_getitem(types.double, 16, points, 0, 8) == 20.0
        assert array_getitem(types.double, 16, points, 1, 0) == 30.0
        assert array_getitem(types.double, 16, points, 1, 8) == 40.0
        #
        lltype.free(points, flavor="raw")


    def test_struct_fields_longlong(self):
        POINT = lltype.Struct('POINT',
                              ('x', rffi.LONGLONG),
                              ('y', rffi.ULONGLONG)
                              )
        y_ofs = 8
        p = lltype.malloc(POINT, flavor='raw')
        p.x = r_longlong(123)
        p.y = r_ulonglong(456)
        addr = rffi.cast(rffi.VOIDP, p)
        assert struct_getfield_longlong(types.slonglong, addr, 0) == 123
        assert struct_getfield_longlong(types.ulonglong, addr, y_ofs) == 456
        #
        v = rffi.cast(lltype.SignedLongLong, r_ulonglong(9223372036854775808))
        struct_setfield_longlong(types.slonglong, addr, 0, v)
        struct_setfield_longlong(types.ulonglong, addr, y_ofs, r_longlong(-1))
        assert p.x == -9223372036854775808
        assert rffi.cast(lltype.UnsignedLongLong, p.y) == 18446744073709551615
        #
        lltype.free(p, flavor='raw')

    def test_struct_fields_float(self):
        POINT = lltype.Struct('POINT',
                              ('x', rffi.DOUBLE),
                              ('y', rffi.DOUBLE)
                              )
        y_ofs = 8
        p = lltype.malloc(POINT, flavor='raw')
        p.x = 123.4
        p.y = 567.8
        addr = rffi.cast(rffi.VOIDP, p)
        assert struct_getfield_float(types.double, addr, 0) == 123.4
        assert struct_getfield_float(types.double, addr, y_ofs) == 567.8
        #
        struct_setfield_float(types.double, addr, 0, 321.0)
        struct_setfield_float(types.double, addr, y_ofs, 876.5)
        assert p.x == 321.0
        assert p.y == 876.5
        #
        lltype.free(p, flavor='raw')

    def test_struct_fields_singlefloat(self):
        POINT = lltype.Struct('POINT',
                              ('x', rffi.FLOAT),
                              ('y', rffi.FLOAT)
                              )
        y_ofs = 4
        p = lltype.malloc(POINT, flavor='raw')
        p.x = r_singlefloat(123.4)
        p.y = r_singlefloat(567.8)
        addr = rffi.cast(rffi.VOIDP, p)
        assert struct_getfield_singlefloat(types.double, addr, 0) == r_singlefloat(123.4)
        assert struct_getfield_singlefloat(types.double, addr, y_ofs) == r_singlefloat(567.8)
        #
        struct_setfield_singlefloat(types.double, addr, 0, r_singlefloat(321.0))
        struct_setfield_singlefloat(types.double, addr, y_ofs, r_singlefloat(876.5))
        assert p.x == r_singlefloat(321.0)
        assert p.y == r_singlefloat(876.5)
        #
        lltype.free(p, flavor='raw')

    def test_windll(self):
        if os.name != 'nt':
            py.test.skip('Run only on windows')
        from rpython.rlib.libffi import WinDLL
        dll = WinDLL('Kernel32.dll')
        sleep = dll.getpointer('Sleep',[types.uint], types.void)
        chain = ArgChain()
        chain.arg(10)
        sleep.call(chain, lltype.Void, is_struct=False)


        
