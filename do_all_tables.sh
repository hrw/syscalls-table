#!/bin/bash

KERNELSRC=$1

TMP=`mktemp`

DEAD_SYSCALLS="afs_syscall|break|ftime|gtty|lock|mpx|oldwait4|prof|profil|putpmsg|security|stty|tuxcall|ulimit|vserver|arm_sync_file_range|utimesat|ni_syscall"

export_headers()
{
	make -s -C ${KERNELSRC} ARCH=${arch} O=${PWD}/headers headers_install &>/dev/null


	grep -E -h "^#define __NR_" ${PWD}/headers/usr/include/asm/unistd*.h ${PWD}/headers/usr/include/asm-generic/unistd.h |
		grep -E -v "(unistd.h|NR3264|__NR_syscall|__SC_COMP|__NR_.*Linux|__NR_FAST)" |
		grep -E -vi "(not implemented|available|unused|reserved|xtensa|spill)" |
		grep -E -v "(__SYSCALL|SYSCALL_BASE|SYSCALL_MASK)" |
		sed -e "s/#define\s*__NR_//g" -e "s/\s.*//g" |
		grep -E -v -w $DEAD_SYSCALLS |
		sort -u >${TMP}
	cat syscall-names.text >>${TMP}
	sed -i '/arch_specific_syscall/d' ${TMP}
	LC_ALL=C sort -u ${TMP} >syscall-names.text
}

generate_table() 
{
	echo -n "$arch "
	echo $arch >> archs-in-kernel

	if [ $bits == 32 ]; then
		extraflags="${extraflags} -D__BITS_PER_LONG=32"
	fi

	gcc list-syscalls.c -U__LP64__ -U__ILP32__ -U__i386__ -D${arch^^} \
		-D__${arch}__ ${extraflags} -I headers/usr/include/ -o list-syscalls &>/dev/null
	./list-syscalls > "tables/syscalls-$arch"
}

rm -f archs-in-kernel

for archdir in $KERNELSRC/arch/*
do 
	arch=`basename $archdir`

	bits=64
	extraflags=

	case ${arch} in
	Kconfig)
		continue;
		;;
	um)
		continue;
		;;
	esac

	export_headers

	case ${arch} in
	arm)
		bits=32
		arch=armoabi		extraflags=				generate_table
		arch=arm		extraflags=-D__ARM_EABI__		generate_table
		;;
	loongarch)
		# 32-bit variant of loongarch may appear
		arch=loongarch64	extraflags=-D_LOONGARCH_SZLONG=64	generate_table
		;;
	mips)
		arch=mips64		extraflags=-D_MIPS_SIM=_MIPS_SIM_ABI64	generate_table
		bits=32
		arch=mipso32		extraflags=-D_MIPS_SIM=_MIPS_SIM_ABI32	generate_table
		arch=mips64n32		extraflags=-D_MIPS_SIM=_MIPS_SIM_NABI32	generate_table
		;;
	powerpc)
										generate_table
		arch=powerpc64							generate_table
		;;
	riscv)
		arch=riscv64		extraflags=-D__LP64__			generate_table
		bits=32
		arch=riscv32		extraflags=-D__SIZEOF_POINTER__=4	generate_table
		;;
	s390)
		bits=32
										generate_table
		bits=64
		arch=s390x							generate_table
		;;
	sparc)
		bits=32
					extraflags=-D__32bit_syscall_numbers__	generate_table
		bits=64
		arch=sparc64		extraflags=-D__arch64__			generate_table
		;;
	tile)
										generate_table
		arch=tile64		extraflags="-D__LP64__ -D__tilegx__"	generate_table
		;;
	x86)
		arch=x86_64		extraflags=-D__LP64__			generate_table
		bits=32
		arch=i386							generate_table
		arch=x32		extraflags=-D__ILP32__			generate_table
		;;
	arc|csky|hexagon|m68k|microblaze|nios2|openrisc|sh|xtensa)
		bits=32 							generate_table
		;;
	*)
		generate_table
		;;
	esac
done

echo ""
