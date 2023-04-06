============
PyPy 4.0.0
============

We're pleased and proud to unleash PyPy 4.0.0, a major update of the PyPy
python 2.7.10 compatible interpreter with a Just In Time compiler.
We have improved `warmup time and memory overhead used for tracing`_, added
`vectorization`_ for numpy and general loops where possible on x86 hardware
(disabled by default),
refactored rough edges in rpython, and increased functionality of numpy.

You can download the PyPy 4.0.0 release here:

    https://pypy.org/download.html

We would like to thank our donors for the continued support of the PyPy
project.

We would also like to thank our contributors (7 new ones since PyPy 2.6.0) and 
encourage new people to join the project. PyPy has many
layers and we need help with all of them: `PyPy`_ and `RPython`_ documentation
improvements, or tweaking popular `modules`_ to run on pypy. 

New Version Numbering
=====================

Since the past release, PyPy 2.6.1, we decided to update the PyPy 2.x.x
versioning directly to PyPy 4.x.x, to avoid confusion with CPython 2.7
and 3.5. Note that this version of PyPy uses the stdlib and implements the
syntax of CPython 2.7.10. 

Benchmarks and a summary of this work appear `here`_

Internal Refactoring: Warmup Time Improvement and Reduced Memory Usage
======================================================================

Numpy
=====

Our implementation of `numpy`_ continues to improve. ndarray and the numeric dtypes
are very close to feature-complete; record, string and unicode dtypes are mostly
supported.  We have reimplemented numpy linalg, random and fft as cffi-1.0
modules that call out to the same underlying libraries that upstream numpy uses.
Please try it out, and let us know what is missing for your code.

CFFI
====

While not applicable only to PyPy, `cffi`_ is arguably our most significant
contribution to the python ecosystem. Armin Rigo continued improving it,
and PyPy reaps the benefits of `cffi-1.3`_: improved manangement of object
lifetimes, __stdcall on Win32, ffi.memmove(), and percolate ``const``,
``restrict`` keywords from cdef to C code.

.. _`warmup time and memory overhead used for tracing`: https://morepypy.blogspot.com/2015/10/pypy-memory-and-warmup-improvements-2.html
.. _`vectorization`: https://pypyvecopt.blogspot.co.at/
.. _`guards`: https://rpython.readthedocs.org/en/latest/glossary.html
.. _`PyPy`: https://doc.pypy.org 
.. _`RPython`: https://rpython.readthedocs.org
.. _`cffi`: https://cffi.readthedocs.org
.. _`cffi-1.3`: https://cffi.readthedocs.org/en/latest/whatsnew.html#v1-3-0
.. _`modules`: https://doc.pypy.org/en/latest/project-ideas.html#make-more-python-modules-pypy-friendly
.. _`help`: https://doc.pypy.org/en/latest/project-ideas.html
.. _`numpy`: https://bitbucket.org/pypy/numpy

What is PyPy?
=============

PyPy is a very compliant Python interpreter, almost a drop-in replacement for
CPython 2.7. It's fast (`pypy and cpython 2.7.x`_ performance comparison).

We also welcome developers of other
`dynamic languages`_ to see what RPython can do for them.

This release supports **x86** machines on most common operating systems
(Linux 32/64, Mac OS X 64, Windows 32, OpenBSD_, freebsd_),
as well as newer **ARM** hardware (ARMv6 or ARMv7, with VFPv3) running Linux.

We also introduce `support for the 64 bit PowerPC`_ hardware, specifically 
Linux running the big- and little-endian variants of ppc64.

.. _`pypy and cpython 2.7.x`: https://speed.pypy.org
.. _OpenBSD: https://cvsweb.openbsd.org/cgi-bin/cvsweb/ports/lang/pypy
.. _freebsd: https://svnweb.freebsd.org/ports/head/lang/pypy/
.. _`dynamic languages`: https://pypyjs.org
.. _`here`: https://morepypy.blogspot.com/2015/10/automatic-simd-vectorization-support-in.html

Other Highlights (since 2.6.1 release two months ago)
=====================================================

* Bug Fixes

  * Applied OPENBSD downstream fixes

  * Fix a crash on non-linux when running more than 20 threads

  * In cffi, ffi.new_handle() is more cpython compliant

  * Accept unicode in functions inside the _curses cffi backend exactly like cpython

  * Fix a segfault in itertools.islice()

  * Use gcrootfinder=shadowstack by default, asmgcc on linux only

  * Fix ndarray.copy() for upstream compatability when copying non-contiguous arrays

  * Fix assumption that lltype.UniChar is unsigned

  * Fix a subtle bug with stacklets on shadowstack

  * When loading dynamic libraries, in case of a certain loading error, retry
    loading the library assuming it is actually a linker script, like on Arch
    and Gentoo

  * Issues reported with our previous release were resolved_ after reports from users on
    our issue tracker at https://bitbucket.org/pypy/pypy/issues or on IRC at
    #pypy

* New features:

  * Add an optimization pass to vectorize loops using x86 SIMD intrinsics.

  * Support __stdcall on Windows in CFFI

  * Improve debug logging when using PYPYLOG=???

  * Deal with platforms with no RAND_egd() in OpenSSL

* Numpy:

  * Add support for ndarray.ctypes

  * Fast path for mixing numpy scalars and floats

  * Add support for creating Fortran-ordered ndarrays

  * Fix casting failures in linalg (by extending ufunc casting)

  * Recognize and disallow (for now) pickling of ndarrays with objects
    embedded in them

* Performance improvements and refactorings:

  * Reuse hashed keys across dictionaries and sets

  * Make the garbage collecter more incremental over external_malloc() calls

  * Share guard resume data where possible which reduces memory usage

  * Fast path for zip(list, list)

  * Factor in field immutability when invalidating heap information

  * Unroll itertools.izip_longest() with two sequences

  * Minor optimizations after analyzing output from `vmprof`_ and trace logs

  * Remove many class attributes in rpython classes

  * Handle getfield_gc_pure* and getfield_gc_* uniformly in heap.py

  * Improve simple trace function performance by lazily calling fast2locals
    and locals2fast only if truly necessary

.. _`vmprof`: https://vmprof.readthedocs.org
.. _resolved: https://doc.pypy.org/en/latest/whatsnew-15.11.0.html

Please try it out and let us know what you think. We welcome feedback,
we know you are using PyPy, please tell us about it!

Cheers

The PyPy Team

