The ``--opt`` or ``-O`` translation option
==========================================

This meta-option selects a default set of optimization
settings to use during a translation.  Usage::

    bin/rpython --opt=#
    bin/rpython -O#

where ``#`` is the desired optimization level.  The valid choices are:

    =============  ========================================================
      Level        Description
    =============  ========================================================
    `--opt=0`      all optimizations off; fastest translation `(*)`_
    `--opt=1`      non-time-consuming optimizations on `(*)`_
    `--opt=size`   minimize the size of the final executable `(*)`_
    `--opt=mem`    minimize the run-time RAM consumption (in-progress)
    `--opt=2`      all optimizations on; good run-time performance
    `--opt=3`      same as `--opt=2`; remove asserts; gcc profiling `(**)`_
    =============  ========================================================

.. _`(*)`:

`(*)`: The levels `0, 1` and `size` use our custom collectors.  The translation
itself is faster and consumes less memory; the final executable is
smaller but slower.  The other levels use one of our built-in `custom
garbage collectors`_.

.. _`(**)`:
    
`(**)`: The level `3` enables gcc profile-driven recompilation when
translating PyPy.

The exact set of optimizations enabled by each level depends
on the backend.  Individual translation targets can also
select their own options based on the level: when translating
PyPy, the level `mem` enables the memory-saving object
implementations in the object space; levels `2` and `3` enable
the advanced object implementations that give an increase in
performance; level `3` also enables gcc profile-driven
recompilation.

The default level is `2`.


.. _`custom garbage collectors`: ../garbage_collection.html
