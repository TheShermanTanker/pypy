===================
PyPy3 v5.2 alpha 1
===================

We're pleased to announce the first alpha release of PyPy3.3 v5.2. This is the
first release of PyPy which targets Python 3.3 (3.3.5) compatibility.

We would like to thank all of the people who donated_ to the `py3k proposal`_
for supporting the work that went into this and future releases.

You can download the PyPy3.3 v5.2 alpha 1 release here:

    https://pypy.org/download.html#python-3-3-5-compatible-pypy3-3-v5-2

Highlights
==========

* Python 3.3.5 support!

  - Being an early alpha release, there are some `missing features`_ such as a
    `PEP 393-like space efficient string representation`_ and `known issues`_
    including performance regressions (e.g. issue `#2305`_). The focus for this
    release has been updating to 3.3 compatibility. Windows is also not yet
    supported.

* `ensurepip`_ is also included (it's only included in CPython 3 >= 3.4).

What is PyPy?
==============

PyPy is a very compliant Python interpreter, almost a drop-in replacement for
CPython 2.7.10 and one day 3.3.5.

We also welcome developers of other `dynamic languages`_ to see what RPython
can do for them.

This release supports:

  * **x86** machines on most common operating systems except Windows
    (Linux 32/64, Mac OS X 64, OpenBSD, FreeBSD),

  * newer **ARM** hardware (ARMv6 or ARMv7, with VFPv3) running Linux,

  * big- and little-endian variants of **PPC64** running Linux,

  * **s390x** running Linux

Please try it out and let us know what you think. We welcome feedback, we know
you are using PyPy, please tell us about it!

We'd especially like to thank these people for their contributions to this
release:

Manuel Jacob, Ronan Lamy, Mark Young, Amaury Forgeot d'Arc, Philip Jenvey,
Martin Matusiak, Vasily Kuznetsov, Matti Picus, Armin Rigo and many others.

Cheers

The PyPy Team

.. _donated: https://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: https://pypy.org/py3donate.html
.. _`PEP 393-like space efficient string representation`: https://bitbucket.org/pypy/pypy/issues/2309/optimized-unicode-representation
.. _`missing features`: https://bitbucket.org/pypy/pypy/issues?status=new&status=open&component=PyPy3+%28running+Python+3.x%29&kind=enhancement
.. _`known issues`: https://bitbucket.org/pypy/pypy/issues?status=new&status=open&component=PyPy3%20%28running%20Python%203.x%29
.. _`#2305`: https://bitbucket.org/pypy/pypy/issues/2305
.. _`ensurepip`: https://docs.python.org/3/library/ensurepip.html#module-ensurepip
.. _`dynamic languages`: https://pypyjs.org
