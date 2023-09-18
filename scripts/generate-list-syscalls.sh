#!/bin/bash

echo "
#include <stdio.h>

#include <asm/unistd.h>

int main(void)
{
"

for syscall in `cat syscall-names.text`
do

	echo "
#ifdef __NR_$syscall
	printf('$syscall\\t%d\\n', __NR_$syscall);
#else
	printf('$syscall\\n');
#endif
"
done

echo "
	return 0;
}
"
