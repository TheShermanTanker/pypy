===========================
What's new in PyPy2.7 5.10+
===========================

.. this is a revision shortly after release-pypy2.7-v5.10.0
.. startrev: 6b024edd9d12


.. branch: mapdict-size-limit

Fix a corner case of mapdict: When an instance is used like a dict (using
``setattr`` and ``getattr``, or ``.__dict__``) and a lot of attributes are
added, then the performance using mapdict is linear in the number of
attributes. This is now fixed (by switching to a regular dict after 80
attributes).


.. branch: 2634_datetime_timedelta_performance

Improve datetime + timedelta performance.

.. branch: memory-accounting

Improve way to describe memory

.. branch: msvc14

Allow compilaiton with Visual Studio 2017 compiler suite on windows


.. branch: call-loopinvariant-into-bridges

Speed up branchy code that does a lot of function inlining by saving one call
to read the TLS in most bridges.

.. branch: rpython-sprint

Refactor in rpython signatures


.. branch: pyparser-improvements

Improve speed of Python parser, improve ParseError messages slightly.

.. branch: ioctl-arg-size

Work around possible bugs in upstream ioctl users, like CPython allocate at
least 1024 bytes for the arg in calls to ``ioctl(fd, request, arg)``. Fixes
issue #2776


.. branch: pyparser-improvements-2

Improve line offsets that are reported by SyntaxError. Improve error messages
for a few situations, including mismatched parenthesis.

.. branch: issue2752

Fix a rare GC bug that was introduced more than one year ago, but was
not diagnosed before issue #2752.

.. branch: gc-hooks

Introduce GC hooks, as documented in doc/gc_info.rst

.. branch: gc-hook-better-timestamp

Improve GC hooks
