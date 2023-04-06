import shutil
import textwrap

from os.path import dirname, join, exists

include = join(dirname(__file__), '..', '..', '..', 'include')
assert exists(include)

def main():
    """Copy/create just enough header information to allow cffi to compile c-extension modules
    """
    python_h = textwrap.dedent("""
        /* Partial C-API headers to allow CFFI C-compiled modules to work with PyPy */
        #include <sys/types.h>
        #include <stdarg.h>

        #ifdef __GNUC__
        #define _GNU_SOURCE 1
        #endif
        #ifndef _WIN32
        # define Py_DEPRECATED(VERSION_UNUSED) __attribute__((__deprecated__))
        # define PyAPI_FUNC(RTYPE) __attribute__((visibility("default"))) RTYPE
        # define PyAPI_DATA(RTYPE) extern PyAPI_FUNC(RTYPE)
        # define Py_LOCAL_INLINE(type) static inline type
        #else
        # define Py_DEPRECATED(VERSION_UNUSED)
        #  define PyAPI_FUNC(RTYPE) __declspec(dllimport) RTYPE
        #  define PyAPI_DATA(RTYPE) extern __declspec(dllimport) RTYPE
        # define Py_LOCAL_INLINE(type) static __inline type __fastcall
        #endif

        typedef void PyObject;
        #ifdef _WIN64
        typedef __int64 Py_ssize_t;
        #else
        typedef __int32 Py_ssize_t;
        #endif
        
        #include <stdarg.h>
        #include <stdio.h>
        #include <string.h>
        #include <assert.h>
        #include <locale.h>
        #include <ctype.h>
        
        /* normally defined in "pythread.h", but we can't include that */
        #define WITH_THREAD
    """)
    if exists(join(include, 'Python.h')):
        return
    with open(join(include, 'Python.h'), 'wt') as fid:
        fid.write(python_h)


if __name__ == '__main__':
    main()

