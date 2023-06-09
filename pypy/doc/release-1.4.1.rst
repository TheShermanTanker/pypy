===============================
PyPy 1.4.1
===============================

We're pleased to announce the 1.4.1 release of PyPy.  This
release consolidates all the bug fixes that occurred since the
previous release.  To everyone that took the trouble to report
them, we want to say thank you.

    https://pypy.org/download.html

What is PyPy
============

PyPy is a very compliant Python interpreter, almost a drop-in
replacement for CPython.  Note that it still only emulates Python
2.5 by default; the ``fast-forward`` branch with Python 2.7
support is slowly getting ready but will only be integrated in
the next release.

In two words, the advantage of trying out PyPy instead of CPython
(the default implementation of Python) is, for now, the
performance.  Not all programs are faster in PyPy, but we are
confident that any CPU-intensive task will be much faster, at
least if it runs for long enough.

Note again that we do support compiling and using C extension
modules from CPython (``pypy setup.py install``).  However, this
is still an alpha feature, and the most complex modules typically
fail for various reasons; others work (e.g. ``PIL``) but take a
serious performance hit.  Also, for Mac OS X see below.

Please note also that PyPy's performance was optimized almost
exclusively on Linux.  It seems from some reports that on Windows
as well as Mac OS X (probably for different reasons) the
performance might be lower.  We did not investigate much so far.


More highlights
===============

* We migrated to Mercurial (thanks to Ronny Pfannschmidt and
  Antonio Cuni) for the effort) and moved to bitbucket.  The new
  command to check out a copy of PyPy is::

        hg clone https://bitbucket.org/pypy/pypy

* Improve a lot the performance of the ``binascii`` module, and
  of ``hashlib.md5`` and ``hashlib.sha``.

* Made sys.setrecursionlimit() a no-op.  Instead, we rely purely
  on the built-in stack overflow detection mechanism, which also
  gives you a RuntimeError -- just not at some exact recursion
  level.

* Fix argument processing (now e.g. ``pypy -OScpass`` works like
  it does on CPython --- if you have a clue what it does there
  ``:-)`` )

* Fix two corner cases in the GC (one in minimark).

* Added some missing built-in functions into the 'os' module.

* Fix ctypes (it was not propagating keepalive information from
  c_void_p).


Cheers,

Armin Rigo, for the rest of the team
