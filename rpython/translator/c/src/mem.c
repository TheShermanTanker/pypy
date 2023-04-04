#include "common_header.h"
#include "src/support.h"
#include <stdlib.h>
#include <stdio.h>

/***  tracking raw mallocs and frees for debugging ***/

#ifdef RPY_ASSERT

struct pypy_debug_alloc_s {
  struct pypy_debug_alloc_s *next;
  void *addr;
  const char *funcname;
};

static struct pypy_debug_alloc_s *pypy_debug_alloc_list = NULL;

RPY_EXTERN
void pypy_debug_alloc_start(void *addr, const char *funcname)
{
  struct pypy_debug_alloc_s *p = malloc(sizeof(struct pypy_debug_alloc_s));
  RPyAssert(p, "out of memory");
  p->next = pypy_debug_alloc_list;
  p->addr = addr;
  p->funcname = funcname;
  pypy_debug_alloc_list = p;
}

RPY_EXTERN
void pypy_debug_alloc_stop(void *addr)
{
  struct pypy_debug_alloc_s **p;
  if (!addr)
	return;
  for (p = &pypy_debug_alloc_list; *p; p = &((*p)->next))
    if ((*p)->addr == addr)
      {
        struct pypy_debug_alloc_s *dying;
        dying = *p;
        *p = dying->next;
        free(dying);
        return;
      }
  RPyAssert(0, "free() of a never-malloc()ed object");
}

RPY_EXTERN
void pypy_debug_alloc_results(void)
{
  Signed count = 0;
  struct pypy_debug_alloc_s *p;
  for (p = pypy_debug_alloc_list; p; p = p->next)
    count++;
  if (count > 0)
    {
      char *env = getenv("PYPY_ALLOC");
      fprintf(stderr, "mem.c: %ld mallocs left", count);
      if (env && *env)
        {
          fprintf(stderr, " (most recent first):\n");
          for (p = pypy_debug_alloc_list; p; p = p->next)
            fprintf(stderr, "    %p  %s\n", p->addr, p->funcname);
        }
      else
        fprintf(stderr, " (use PYPY_ALLOC=1 to see the list)\n");
    }
}

#endif /* RPY_ASSERT */


