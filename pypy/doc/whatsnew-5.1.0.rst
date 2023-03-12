=========================
What's new in PyPy 5.1
=========================

.. this is a revision shortly after release-5.0
.. startrev: b238b48f9138

.. branch: remove-py-log

Replace py.log with something simpler, which should speed up logging

.. branch: where_1_arg

Implemented numpy.where for 1 argument (thanks sergem)

.. branch: fix_indexing_by_numpy_int

Implement yet another strange numpy indexing compatibility; indexing by a scalar 
returns a scalar

.. branch: fix_transpose_for_list_v3

Allow arguments to transpose to be sequences

.. branch: win32-lib-name

.. branch: remove-frame-forcing-in-executioncontext

.. branch: rposix-for-3

Wrap more POSIX functions in `rpython.rlib.rposix`.

.. branch: cleanup-includes

Remove old uneeded numpy headers, what is left is only for testing. Also 
generate pypy_numpy.h which exposes functions to directly use micronumpy
ndarray and ufuncs

.. branch: rposix-for-3

Reuse rposix definition of TIMESPEC in rposix_stat, add wrapper for fstatat().
This updates the underlying rpython functions with the ones needed for the 
py3k branch
 
.. branch: numpy_broadcast

Add broadcast to micronumpy
