from pypy.module.imp import importing
from rpython.rlib import streamio
from pypy.interpreter.error import oefmt
from pypy.interpreter.gateway import unwrap_spec
from pypy.interpreter.pycode import PyCode
from pypy.module._io.interp_iobase import W_IOBase
from pypy.interpreter.streamutil import wrap_streamerror
from pypy.interpreter.error import OperationError


def extension_suffixes(space):
    suffixes_w = []
    so_ext = importing.get_so_extension(space)
    if "powerpc64le" in so_ext or "ppc_64" in so_ext:
        # force adding a backward-compatible suffix (issue 3833)
        suffixes_w.append(space.newtext(".pypy39-pp73-ppc_64-linux-gnu.so"))
        suffixes_w.append(space.newtext(".pypy39-pp73-powerpc64le-linux-gnu.so"))
    else:   #if space.config.objspace.usemodules.cpyext:
        suffixes_w.append(space.newtext(so_ext))
    return space.newlist(suffixes_w)

def get_magic(space):
    x = importing.get_pyc_magic(space)
    a = x & 0xff
    x >>= 8
    b = x & 0xff
    x >>= 8
    c = x & 0xff
    x >>= 8
    d = x & 0xff
    return space.newbytes(chr(a) + chr(b) + chr(c) + chr(d))

def get_tag(space):
    """get_tag() -> string
    Return the magic tag for .pyc files."""
    return space.newtext(importing.PYC_TAG)

def get_file(space, w_file, filename, filemode):
    if space.is_none(w_file):
        try:
            return streamio.open_file_as_stream(filename, filemode)
        except streamio.StreamErrors as e:
            # XXX this is not quite the correct place, but it will do for now.
            # XXX see the issue which I'm sure exists already but whose number
            # XXX I cannot find any more...
            raise wrap_streamerror(space, e)
    else:
        w_iobase = space.interp_w(W_IOBase, w_file)
        # XXX: not all W_IOBase have a fileno method: in that case, we should
        # probably raise a TypeError?
        fd = space.int_w(space.call_method(w_iobase, 'fileno'))
        return streamio.fdopen_as_stream(fd, filemode)

def create_dynamic(space, w_spec, w_file=None):
    if not importing.has_so_extension(space):
        raise oefmt(space.w_ImportError, "Not implemented")
    from pypy.module.cpyext.api import create_extension_module
    # NB. cpyext.api.create_extension_module() can also delegate to _cffi_backend
    return create_extension_module(space, w_spec)

def create_builtin(space, w_spec):
    w_name = space.getattr(w_spec, space.newtext("name"))
    name = space.text0_w(w_name)
    # force_init is needed to make reload actually reload instead of just
    # using the already-present module in sys.modules.

    # If the module is already in sys.modules, it must be a reload, so
    # we want to reuse (and reinitialize) the existing module object
    reuse = space.finditem(space.sys.get('modules'), w_name) is not None
    return space.getbuiltinmodule(name, force_init=True, reuse=reuse)

def exec_dynamic(space, w_mod):
    from pypy.module.cpyext.api import exec_extension_module
    exec_extension_module(space, w_mod)

def exec_builtin(space, w_mod):
    return

def init_frozen(space, w_name):
    return None

def is_builtin(space, w_name):
    try:
        name = space.text0_w(w_name)
    except OperationError:
        return space.newint(0)

    if name not in space.builtin_modules:
        return space.newint(0)
    if space.finditem(space.sys.get('modules'), w_name) is not None:
        return space.newint(-1)   # cannot be initialized again
    return space.newint(1)

def is_frozen(space, w_name):
    name = space.text_w(w_name)
    if name in ("_frozen_importlib", "_frozen_importlib_external", "zipimport",
                # For tests, not implemented on PyPy
                "__hello__", "__phello__", "_phello__.spam"):
        return space.w_True
    return space.w_False

def use_frozen(space):
    """private function that allows never using frozen modules"""
    from pypy.module.imp.state import State
    state = space.fromcache(State)
    override = state.override_frozen_modules
    if override > 0:
        return True
    elif override < 0:
        return False
    # TODO: when built with Py_DEBUG, return False
    return True


def list_frozen_module_names(space):
    always_freeze = space.newlist([space.newtext(s) for s in [
        "_frozen_importlib", "_frozen_importlib_external", "zipimport",
        ]])

    frozen = always_freeze
    # issue 5098: also freeze test and stdlib modules
    if use_frozen(space):
        # For tests, not implemented on PyPy
        # frozen +=  ["__hello__", "__phello__", "_phello__.spam"]
        # For speedups
        # frozen += stdlib_frozens
        pass
    return frozen

def get_frozen_object(space, w_name):
    raise oefmt(space.w_ImportError,
                "No such frozen object named %R", w_name)

def is_frozen_package(space, w_name):
    return space.w_False

def find_frozen(space, w_name):
    return space.w_None
    # TODO: use the stdlibfrozens and test frozens


#__________________________________________________________________

def lock_held(space):
    if space.config.objspace.usemodules.thread:
        return space.newbool(importing.getimportlock(space).lock_held_by_anyone())
    else:
        return space.w_False

def acquire_lock(space):
    if space.config.objspace.usemodules.thread:
        importing.getimportlock(space).acquire_lock()

def release_lock(space):
    if space.config.objspace.usemodules.thread:
        importing.getimportlock(space).release_lock(silent_after_fork=False)

def reinit_lock(space):
    if space.config.objspace.usemodules.thread:
        importing.getimportlock(space).reinit_lock()

@unwrap_spec(pathname='fsencode')
def fix_co_filename(space, w_code, pathname):
    code_w = space.interp_w(PyCode, w_code)
    importing.update_code_filenames(space, code_w, pathname)


@unwrap_spec(magic=int, content='bytes')
def source_hash(space, magic, content):
    from rpython.rlib.rsiphash import siphash24_with_key
    from rpython.rlib.rarithmetic import r_uint64
    h = siphash24_with_key(content, r_uint64(magic))
    res = [b"x"] * 8
    for i in range(8):
        res[i] = chr(h & 0xff)
        h >>= 8
    assert not h
    return space.newbytes(b"".join(res))
