=======================
PyPy 1.3: Stabilization
=======================

Hello.

We're please to announce release of PyPy 1.3.

We're pleased to announce alpha support for loading CPython extension
modules written in C. While the main purpose of this release is increased
stability, this feature is in alpha stage and it is not yet suited for
production environments.

Highlights of this release
==========================

* We introduced support for CPython extension modules written in C. As of now,
  this support is in alpha, and it's very unlikely unaltered C extensions will
  work out of the box, due to missing functions or refcounting details. The
  support is disable by default, so you have to do::

   import cpyext

  before trying to import any .so file. Also, libraries are source-compatible
  and not binary-compatible. That means you need to recompile binaries, using
  for example::

   python setup.py build

  Details may vary, depending on your build system. Make sure you include
  the above line at the beginning of setup.py or put it in your PYTHONSTARTUP.

  This is alpha feature. It'll likely segfault. You have been warned!

Cheers,
Maciej Fijalkowski, Armin Rigo, Alex Gaynor, Amaury Forgeot d'Arc and the PyPy team
