import dis
from pypy.interpreter.reverse_debugging import *
from pypy.interpreter import reverse_debugging
from rpython.rlib import revdb, rpath
from hypothesis import given, strategies, example


class FakeCode:
    hidden_applevel = False
    def __init__(self, co_code='', co_lnotab='', co_filename='?'):
        self.co_firstlineno = 43
        self.co_code = co_code
        self.co_lnotab = co_lnotab
        self.co_revdb_linestarts = None
        self.co_filename = co_filename


@given(strategies.binary())
@example("\x01\x02\x03\x04"
         "\x00\xFF\x20\x30\x00\xFF\x00\x40"
         "\xFF\x00\x0A\x0B\xFF\x00\x0C\x00")
def test_build_co_revdb_linestarts(lnotab):
    if len(lnotab) & 1:
        lnotab = lnotab + '\x00'   # make the length even
    code = FakeCode("?" * sum(map(ord, lnotab[0::2])), lnotab)
    lstart = build_co_revdb_linestarts(code)
    assert lstart is code.co_revdb_linestarts

    expected_starts = set()
    for addr, lineno in dis.findlinestarts(code):
        expected_starts.add(addr)

    next_start = len(code.co_code)
    for index in range(len(code.co_code), -1, -1):
        if index in expected_starts:
            next_start = index
        assert lstart[index] == chr(next_start - index
                                    if next_start - index <= 255
                                    else 255)

class FakeFrame:
    def __init__(self, code):
        self.__code = code
    def getcode(self):
        return self.__code

def check_add_breakpoint(input, curfilename=None,
                         expected_funcname=None,
                         expected_fileline=None,
                         expected_output=None,
                         expected_chbkpt=None):
    dbstate.__dict__.clear()
    prev = revdb.send_answer, reverse_debugging.fetch_cur_frame
    try:
        messages = []
        def got_message(cmd, arg1=0, arg2=0, arg3=0, extra=""):
            messages.append((cmd, arg1, arg2, arg3, extra))
        def my_cur_frame():
            assert curfilename is not None
            return FakeFrame(FakeCode(co_filename=curfilename))
        revdb.send_answer = got_message
        reverse_debugging.fetch_cur_frame = my_cur_frame
        add_breakpoint(input, 5)
    finally:
        revdb.send_answer, reverse_debugging.fetch_cur_frame = prev

    if expected_funcname is None:
        assert dbstate.breakpoint_funcnames is None
    else:
        assert dbstate.breakpoint_funcnames == {expected_funcname: 5}

    if expected_fileline is None:
        assert dbstate.breakpoint_filelines is None
    else:
        filename, lineno = expected_fileline
        assert dbstate.breakpoint_filelines == {filename: {lineno: 5}}

    got_output = None
    got_chbkpt = None
    if messages:
        assert len(messages) <= 1
        if messages[0][0] == revdb.ANSWER_TEXT:
            got_output = messages[0][-1]
        if messages[0][0] == revdb.ANSWER_CHBKPT:
            assert messages[0][1] == 5
            got_chbkpt = messages[0][-1]

    assert got_output == expected_output
    assert got_chbkpt == expected_chbkpt

def fullpath(path):
    return rpath.rnormpath(rpath.rabspath(path))

def test_add_breakpoint():
    check_add_breakpoint('', expected_output="Empty breakpoint name\n")
    check_add_breakpoint('foo42', expected_funcname="foo42")
    check_add_breakpoint('foo.bar', expected_funcname="foo.bar",
        expected_output='Note: "foo.bar()" doesn''t look like a function name.'
                        ' Setting breakpoint anyway\n')
    check_add_breakpoint('<foo.bar>', expected_funcname="<foo.bar>")
    check_add_breakpoint('42', curfilename='abcd',
                         expected_fileline=('abcd', 42),
                         expected_chbkpt='abcd:42')
    check_add_breakpoint(':42', curfilename='abcd',
                         expected_fileline=('abcd', 42),
                         expected_chbkpt='abcd:42')
    check_add_breakpoint('abcd:42', expected_fileline=('abcd', 42),
        expected_output='Note: "abcd" doesnt look like a co_filename.'
                        ' Setting breakpoint anyway\n')
    full = fullpath('abcd.py')
    check_add_breakpoint('abcd.py:42',
                         expected_fileline=(full, 42),
                         expected_chbkpt='%s:42' % full)
    check_add_breakpoint('%s:42' % full,
                         expected_fileline=(full, 42))
