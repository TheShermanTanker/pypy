==================================
PyPy 1.2: Just-in-Time Compilation
==================================

Welcome to the PyPy 1.2 release.  The highlight of this release is
to be the first that ships with a Just-in-Time compiler that is
known to be faster than CPython (and unladen swallow) on some
real-world applications (or the best benchmarks we could get for
them).  The main theme for the 1.2 release is speed.

Main site:

    https://pypy.org/


Highlights of This Release
==========================

* Various interpreter optimizations that improve performance
  as well as help save memory.

* Introducing a new PyPy website at https://pypy.org/ , made by
  tav and improved by the PyPy team.

* Introducing https://speed.pypy.org/ , a new service that
  monitors our performance nightly, made by Miquel Torres.

* There will be ubuntu packages on "PyPy's PPA" made by
  Bartosz Skowron; however various troubles prevented us from
  having them as of now.


If you want to try PyPy, go to the "download page" on our excellent
new site at https://pypy.org/download.html and find the binary for
your platform. If the binary does not work (e.g. on Linux, because
of different versions of external .so dependencies), or if your
platform is not supported, you can try building from the source.


What is PyPy?
=============

Technically, PyPy is both a Python interpreter implementation and an
advanced compiler, or more precisely a framework for implementing
dynamic languages and generating virtual machines for them.

Socially, PyPy is a collaborative effort of many individuals working
together in a distributed and sprint-driven way since 2003.  PyPy
would not have gotten as far as it has without the coding, feedback
and general support from numerous people.


The PyPy release team,
    Armin Rigo, Maciej Fijalkowski and Amaury Forgeot d'Arc

Together with
    Antonio Cuni, Carl Friedrich Bolz, Holger Krekel and
    Samuele Pedroni

and many others:
    https://codespeak.net/pypy/dist/pypy/doc/contributor.html
