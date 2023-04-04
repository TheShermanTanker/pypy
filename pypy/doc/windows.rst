Translating on Windows
======================

RPython is supported on Windows platforms, starting with Windows 2000.
The following text gives some hints about how to translate a interpreter
written in RPython, using PyPy as an example.

To build pypy-c you need a working python environment, and a C compiler.
It is possible to translate with a CPython 2.6 or 2.7, but this is not
the preferred way, because it will take a lot longer to run – depending
on your architecture, between two and three times as long. So head to
`our downloads`_ and get the latest stable version.

Microsoft Visual Studio is the only supported compiler.

.. _our downloads: https://www.pypy.org/download.html


What Compiler to use and How to find it?
----------------------------------------
The first stumbling block when building something for Python on windows is
how to discover the path to the compiler, headers, and libraries. One can
install many versions of the MSVC compiler tools, from stand-alone build
tools to full blown Visual Studio IDE installations. Each of these use cases
put the compiler at different locations, and the layout changes from time to
time.

The ``distutils`` package, located in the stdlib, is the natural place to put
this discovery code, but it is frozen by the python version. The pip-
installable ``setuptools`` can move faster to adapt to new tools. So the first
thing that will happen after building PyPy is it will install pip and download
``setuptools``, then it will build the cffi modules used in stdlib.
PyPy has a chicken and egg problem: in order to compile something we need
``setuptools``, but in order to get ``setuptools`` we need pip which requires
``_ssl``, and ``_ssl`` must be compiled. So PyPy vendors in a copy of
``msvc.py`` in ``rpython/tools/setuptools_msvc.py``.

PyPy will prefer to compile with the latest MSVC compiler it can find, which is
a departure from CPython's desire to compile with the compiler used to compile
the exe in use.

Translating PyPy with Visual Studio
-----------------------------------

We routinely test translation of PyPy using Visual Studio 2019, MSVC160.
Other configurations may work as well. You must use at least Visual Studio
2012.

The translation scripts will set up the appropriate environment variables
for the compiler, so you do not need to run vcvars before translation.
They will pick the most recent Visual Studio
compiler they can find.  In addition, the target architecture
(32 bits, 64 bits) is automatically selected.  A 32 bit build can only be built
using a 32 bit Python and vice versa. By default the interpreter is built using
the Multi-threaded DLL (/MD) runtime environment.

**Note:** The RPython translator requires a special 64 bit Python, see below

Python and a C compiler are all you need to build pypy, but it will miss some
modules that relies on third-party libraries.  See below how to get
and build them.

Please see the :doc:`non-windows instructions <build>` for more information, especially note
that translation is RAM-hungry. A standard translation requires around 4GB, so
special preparations are necessary, or you may want to use the following method
to reduce memory usage at the price of a slower translation::

    set PYPY_GC_MAX_DELTA=200MB
    pypy ../../rpython/bin/rpython targetpypystandalone
    set PYPY_GC_MAX_DELTA=
    # This is done as part of translation
    PYTHONPATH=../.. ./pypy-c ../../lib_pypy/pypy_tools/build_cffi_imports.py

Preparing Windows for the large build
-------------------------------------

Normally 32bit programs are limited to 2GB of memory on Windows. It is
possible to raise this limit to almost 4GB on Windows 64bit.

You need to execute::

    <path-to-visual>\vc\vcvars.bat
    editbin /largeaddressaware translator.exe

where ``translator.exe`` is the pypy.exe or cpython.exe you will use to
translate with. This is done by default during PyPy translation, so it should
Just Work.


Installing external packages
----------------------------

We uses a subrepository_ inside pypy to hold binary compiled versions of the
build dependencies for windows. As part of the `rpython` setup stage, environment
variables will be set to use these dependencies. The repository has a README
file on how to replicate, and a branch for each supported platform. You may run
the `get_externals.py` utility to checkout the proper branch for your platform
and PyPy version.

.. _subrepository: https://foss.heptapod.net/pypy/externals

.. _libffi source files: https://sourceware.org/libffi/


What is missing for a full 64-bit translation
---------------------------------------------

This is a placeholder for old links to this topic. We have :ref:`solved the
64-bit translation problems <windows64>` and there are nightly builds of 64-bit windows.

