=========================
What's new in PyPy2.7 5.3
=========================

.. this is a revision shortly after release-5.1
.. startrev: aa60332382a1

.. branch: techtonik/introductionrst-simplify-explanation-abo-1460879168046

.. branch: gcheader-decl

Reduce the size of generated C sources.


.. branch: remove-objspace-options

Remove a number of options from the build process that were never tested and
never set. Fix a performance bug in the method cache.

.. branch: share-mapdict-methods-2

Reduce generated code for subclasses by using the same function objects in all
generated subclasses.

.. branch: oefmt

.. branch: gc-del-3

Add rgc.FinalizerQueue, documented in pypy/doc/discussion/finalizer-order.rst.
It is a more flexible way to make RPython finalizers.

.. branch: cleanups

.. branch: use-gc-del-3

Use the new rgc.FinalizerQueue mechanism to clean up the handling of
``__del__`` methods.  Fixes notably issue #2287.  (All RPython
subclasses of W_Root need to use FinalizerQueue now.)

.. branch: ufunc-outer

Implement ufunc.outer on numpypy

.. branch: verbose-imports

Support ``pypy -v``: verbose imports.  It does not log as much as
cpython, but it should be enough to help when debugging package layout
problems.

.. branch: syntax_fix

.. branch: nonmovable-list

Add a way to ask "give me a raw pointer to this list's
items".  Only for resizable lists of primitives.  Turns the GcArray
nonmovable, possibly making a copy of it first.
