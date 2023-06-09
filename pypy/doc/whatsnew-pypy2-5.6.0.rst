=========================
What's new in PyPy2.7 5.6
=========================

.. this is a revision shortly after release-pypy2.7-v5.4
.. startrev: 522736f816dc

.. branch: rpython-resync

Backport rpython changes made directly on the py3k and py3.5 branches.

.. branch: search-path-from-libpypy

The compiled pypy now looks for its lib-python/lib_pypy path starting
from the location of the *libpypy-c* instead of the executable. This is
arguably more consistent, and also it is what occurs anyway if you're
embedding pypy.  Linux distribution packagers, take note!  At a minimum,
the ``libpypy-c.so`` must really be inside the path containing
``lib-python`` and ``lib_pypy``.  Of course, you can put a symlink to it
from somewhere else.  You no longer have to do the same with the
``pypy`` executable, as long as it finds its ``libpypy-c.so`` library.

.. branch: _warnings

CPython allows warning.warn(('something', 1), Warning), on PyPy this
produced a "expected a readable buffer object" error. Test and fix.

.. branch: stricter-strip

CPython rejects 'a'.strip(buffer(' ')); only None, str or unicode are
allowed as arguments. Test and fix for str and unicode

.. branch: faulthandler

Port the 'faulthandler' module to PyPy default.  This module is standard
in Python 3.3 but can also be installed from CPython >= 2.6 from PyPI.

.. branch: better-error-missing-self

Improve the error message when the user forgot the "self" argument of a method.


.. fb6bb835369e

Change the ``timeit`` module: it now prints the average time and the standard
deviation over 7 runs by default, instead of the minimum. The minimum is often
misleading.

.. branch: unrecursive-opt

Make optimiseopt iterative instead of recursive so it can be reasoned about
more easily and debugging is faster.

.. branch: Tiberiumk/fix-2412-1476011166874
.. branch: stdlib-2.7.12

Update stdlib to version 2.7.12


.. branch: fix-struct-unpack-Q

Improve compatibility with CPython in the ``struct`` module. In particular,
``struct.unpack`` now returns an ``int`` whenever the returned value fits,
while previously it always returned a ``long`` for certains format codes such
as ``Q`` (and also ``I``, ``L`` and ``q`` on 32 bit)

.. branch: zarch-simd-support

s390x implementation for vector operations used in VecOpt

.. branch: ppc-vsx-support

PowerPC implementation for vector operations used in VecOpt

.. branch: newinitwarn

Match CPython's stricter handling of ``__new__``/``__init__`` arguments

.. branch: openssl-1.1

Support for OpenSSL version 1.1 (in addition to version 1.0).
Tested on Linux (1.1, 1.0), on Win32, and Mac (1.0 only)
