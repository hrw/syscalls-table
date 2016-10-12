#/bin/bash

TMP=`mktemp`

grep "#define __NR_" /usr/include/asm-generic/unistd.h /usr/include/asm/unistd.h | \
        grep -v NR3264 | \
        grep -v __NR_syscall | \
        egrep -v "SYSCALL_BASE" | \
        grep -v arch_specific_syscall  | \
        cut -d" " -f2 | \
        sed -e "s/__NR_//g" >$TMP
cat syscall-names.text >>$TMP
LC_ALL=C sort -u $TMP >syscall-names.text

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
	printf('$syscall\\\t%d\\\n', __NR_$syscall);
#else
	printf('$syscall\\\n');
#endif
"
done

echo "
	return 0;
}
"
