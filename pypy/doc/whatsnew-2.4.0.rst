=======================
What's new in PyPy 2.4+
=======================

.. this is a revision shortly after release-2.3.x
.. startrev: ca9b7cf02cf4

.. branch: fix-bytearray-complexity

Bytearray operations no longer copy the bytearray unnecessarily

Added support for ``__getitem__``, ``__setitem__``, ``__getslice__``,
``__setslice__``,  and ``__len__`` to RPython

.. branch: stringbuilder2-perf

Give the StringBuilder a more flexible internal structure, with a
chained list of strings instead of just one string. This make it
more efficient when building large strings, e.g. with cStringIO().

.. branch: disable_pythonapi

Remove non-functioning ctypes.pyhonapi and ctypes.PyDLL, document this
incompatibility with cpython. Recast sys.dllhandle to an int.

.. branch: scalar-operations

Fix performance regression on ufunc(<scalar>, <scalar>) in numpy.

.. branch: pytest-25

Update our copies of py.test and pylib to versions 2.5.2 and 1.4.20, 
respectively.

.. branch: split-ast-classes

Classes in the ast module are now distinct from structures used by the compiler.

.. branch: stdlib-2.7.8

Upgrades from 2.7.6 to 2.7.8

.. branch: cpybug-seq-radd-rmul

Fix issue #1861 - cpython compatability madness
