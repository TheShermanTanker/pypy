"""
Implementation of the 'sys._current_frames()' routine.
"""


def _current_frames(space):
    """_current_frames() -> dictionary

    Return a dictionary mapping each current thread T's thread id to T's
    current stack frame.  Functions in the traceback module can build the
    call stack given such a frame.

    This function should be used for specialized purposes only."""
    w_result = space.newdict()
    ecs = space.threadlocals.getallvalues()
    for thread_ident, ec in ecs.items():
        w_topframe = ec.gettopframe_nohidden()
        if w_topframe is None:
            continue
        space.setitem(w_result,
                      space.newint(thread_ident),
                      w_topframe)
    return w_result
