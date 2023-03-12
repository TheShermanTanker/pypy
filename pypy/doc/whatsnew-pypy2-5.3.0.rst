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

.. branch: share-cpyext-cpython-api

.. branch: cpyext-auto-gil

CPyExt tweak: instead of "GIL not held when a CPython C extension module
calls PyXxx", we now silently acquire/release the GIL.  Helps with
CPython C extension modules that call some PyXxx() functions without
holding the GIL (arguably, they are theorically buggy).

.. branch: cpyext-test-A

Get the cpyext tests to pass with "-A" (i.e. when tested directly with
CPython).

.. branch: oefmt

.. branch: cpyext-werror

Compile c snippets with -Werror in cpyext

.. branch: gc-del-3

Add rgc.FinalizerQueue, documented in pypy/doc/discussion/finalizer-order.rst.
It is a more flexible way to make RPython finalizers.

.. branch: unpacking-cpython-shortcut

.. branch: cleanups

.. branch: cpyext-more-slots

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

.. branch: cpyext-macros-cast

Fix some warnings when compiling CPython C extension modules

.. branch: syntax_fix

.. branch: nonmovable-list

Add a way to ask "give me a raw pointer to this list's
items".  Only for resizable lists of primitives.  Turns the GcArray
nonmovable, possibly making a copy of it first.

.. branch: cpyext-ext

Finish the work already partially merged in cpyext-for-merge. Adds support
for ByteArrayObject using the nonmovable-list, which also enables
buffer(bytearray(<some-list>)) 
