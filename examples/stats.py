#!/usr/bin/python3

import system_calls

popular_syscalls = {}

syscalls = system_calls.syscalls()

for syscall_name in syscalls.names():
    counter = 0

    for arch in syscalls.archs():
        try:
            syscalls.get(syscall_name, arch)
            counter += 1
        except system_calls.NotSupportedSystemCall:
            pass

    try:
        popular_syscalls[counter].append(syscall_name)
    except KeyError:
        popular_syscalls[counter] = []
        popular_syscalls[counter].append(syscall_name)

amount_of_archs = len(syscalls.archs())

for amount in range(1, amount_of_archs + 1):
    try:
        tmp = popular_syscalls[amount]
        print(f"System calls supported on {amount} of {amount_of_archs} "
              "architectures:")
        for syscall in popular_syscalls[amount]:
            print(f"\t{syscall}")
        print("\n")
    except KeyError:
        pass
