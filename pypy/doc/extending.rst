Writing extension modules for pypy
==================================

This document tries to explain how to interface the PyPy python interpreter
with any external library.

Right now, there are the following possibilities of providing
third-party modules for the PyPy python interpreter (in order, from most
directly useful to most messy to use with PyPy):

* Write them in pure Python and use CFFI_.

* Write them in pure Python and use ctypes_.

* Write them as `RPython mixed modules`_.


CFFI
----

CFFI__ is the recommended way.  It is a way to write pure Python code
that accesses C libraries.  The idea is to support either ABI- or
API-level access to C --- so that you can sanely access C libraries
without depending on details like the exact field order in the C
structures or the numerical value of all the constants.  It works on
both CPython (as a separate ``python -mpip install cffi``) and on PyPy, where it
is included by default.

See the documentation here__.

.. __: https://cffi.readthedocs.org/
.. __: https://cffi.readthedocs.org/


CTypes
------

The goal of the ctypes module of PyPy is to be as compatible as possible
with the `CPython ctypes`_ version.  It works for large examples, such
as pyglet.  PyPy's implementation is not strictly 100% compatible with
CPython, but close enough for most cases.
More (but older) information is available :doc:`here <discussion/ctypes-implementation>`.
Also, ctypes' performance is not as good as CFFI's.

.. _CPython ctypes: https://docs.python.org/library/ctypes.html

PyPy implements ctypes as pure Python code around two built-in modules
called ``_rawffi`` and ``_rawffi.alt``, which give a very low-level binding to
the C library libffi_.  Nowadays it is not recommended to use directly
these two modules.

.. _libffi: https://sourceware.org/libffi/


RPython Mixed Modules
---------------------

This is the internal way to write built-in extension modules in PyPy.
It cannot be used by any 3rd-party module: the extension modules are
*built-in*, not independently loadable DLLs.


