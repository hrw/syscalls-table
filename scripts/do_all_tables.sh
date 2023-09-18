#!/bin/bash

KERNELSRC=$1

export_headers()
{
	make -s -C ${KERNELSRC} ARCH=${arch} O=${PWD}/headers headers_install &>/dev/null
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
