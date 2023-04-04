/* Thread implementation */
#include "src/thread.h"


#ifdef PYPY_MAKEFILE
/* This is needed for having 'pypy_threadlocal_s' defined, which is needed
   for _rpygil_get_my_ident */
#  include "common_header.h"
#  include "structdef.h"
#endif


#ifdef _WIN32
#include "src/thread_nt.c"
#else
#include "src/thread_pthread.c"
#endif
