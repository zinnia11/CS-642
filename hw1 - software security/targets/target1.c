#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int bar(char *arg, char *out)
{
  strcpy(out, arg);
  fprintf(stderr, "bar() addr of out hex = %x\n", out);
  fprintf(stderr, "bar() addr of arg hex = %x\n", arg);
  fprintf(stderr, "bar() contents of arg hex = %x\n", *arg);
  return 0;
}

int foo(char *argv[])
{
  char buf[180];
  bar(argv[1], buf);
}

int main(int argc, char *argv[])
{
  if (argc != 2)
    {
      fprintf(stderr, "target1: argc != 2\n");
      exit(EXIT_FAILURE);
    }
  foo(argv);
  return 0;
}
