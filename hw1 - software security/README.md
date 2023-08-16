# CS642-HW1

This homework assignment needs you to understand vulnerabilities in 6 target programs. The first 5 are required; the 6th one is for extra credit. 

# The Targets
The targets/ directory contains the source code for the vulnerable targets, along with a Makefile for building them.

Your exploits should assume that the compiled target programs are installed setuid-root in /tmp -->  /tmp/target0, /tmp/target1, etc.

To build the targets, change to the targets/ directory and type make on the command line; the Makefile will take care of building the targets.

To install the target binaries in /tmp, run:

```
  make install
```

To make the target binaries setuid-root, run:

```
  su # will need to enter root password
  make setuid
  exit  # to get out of the root shell
```

Once you've run make setuid use exit to return to your user shell. 

Keep in mind that it'll be easier to debug the exploits if the targets aren't setuid. (See below for more on debugging.) If an exploit succeeds in getting a user shell on a non-setuid target in /tmp, it should succeed in getting a root shell on that target when it is setuid. (But be sure to test that way, too, before submitting your solutions!) 

# The Exploits

The sploits/contains skeleton source for the exploits which you are to write, along with a Makefile for building them. Also included is shellcode.h, which gives Aleph One's shellcode (code which leads a vulnerable target to a shell).

# The Assignment

You are to write exploits for vulnerable targets, with one exploit per target.

1. The goal of sploit0 is different from the rest of the exploits. Take a look at target0.c, the output is "Grade = F" for any string (<30 bytes) you pass. Your goal as an attacker is to hijack the control flow of target0 to print "Grade = A". Use sploit0.c to generate and pass a "string" that is going to aid you in obtaining the desired grade, which is A obviously.
2. The rest of the exploits (sploit1 through sploit5), when run in the virtual machine with its target installed setuid-root in /tmp, should yield a root shell (/bin/sh).
3. For full credit you  must provide an explanation in the sploit[0-5].txt files. The explanation should be sufficiently detailed to explain how you arrived at your solution.
4. We will grade each of your exploits implementation on an all or nothing basis. So make sure your code works before submission!
5. Once again, sploit0-4 are required; sploit5 is extra credit. The total points for sploit0 is 10, each of sploit1-3 is worth 20 pts, and sploit4 is worth 30 pts. sploit5 is 20 points extra credit.

# Hints

To understand what's going on, it is helpful to run code through gdb. See the GDB tips section below.

Make sure that your exploits work within the provided virtual machine.

# GDB Tips

Look up how to use the disassemble and stepi commands.

You may find the x command useful to examine memory (and the different ways you can print the contents such as /a /i after x). The info register command is helpful in printing out the contents of registers such as ebp and esp.

A useful way to run gdb is to use the -e and -s command line flags; for example, the command gdb -e sploit3 -s /tmp/target3 in the VM tells gdb to execute sploit3 and use the symbol file in target3. These flags let you trace the execution of the target3 after the sploit's memory image has been replaced with the target's through the execve system call.

When running gdb using these command line flags, you should follow the following procedure for setting breakpoints and debugging memory:

Tell gdb to notify you on exec(), by issuing the command catch exec
Run the program. gdb will execute the sploit until the execve syscall, then return control to you
Set any breakpoints you want in the target
Resume execution by telling gdb continue (or just c).
If you try to set breakpoints before the exec boundary, you will get a segfault.

If you wish, you can instrument the target code with arbitrary assembly using the __asm__ () pseudofunction, to help with debugging. Be sure, however, that your final exploits work against the unmodified targets, since these we will use these in grading.

# Warnings
Aleph One gives code that calculates addresses on the target's stack based on addresses on the exploit's stack. Addresses on the exploit's stack can change based on how the exploit is executed (working directory, arguments, environment, etc.); during grading, we do not guarantee to execute your exploits exactly the same way bash does.  You must therefore hard-code target stack locations in your exploits. You should *not* use a function such as get_sp() in the exploits you hand in.

(In other words, during grading the exploits may be run with a different environment and different working directory than one would get by logging in as user, changing directory to ~/hw1/sploits, and running ./sploit1, etc.; your exploits must work even so.)

Your exploit programs should not take any command-line arguments.
