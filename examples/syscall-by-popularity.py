#!/usr/bin/python3

"""
Print syscalls in 'popularity' order.

From entries supported on one architecture to supported on every one.
"""

import system_calls

syscalls = system_calls.syscalls()

syscalls_count = {}

for syscall_name in syscalls.names():

    syscalls_count[syscall_name] = {"amount": 0, "archs": []}

    for arch in syscalls.archs():
        try:
            syscalls.get(syscall_name, arch)
            syscalls_count[syscall_name]["amount"] += 1
            syscalls_count[syscall_name]["archs"].append(arch)
        except system_calls.NotSupportedSystemCall:
            pass

for amount in range(1, len(syscalls.archs()) + 1):
    for syscall_name in syscalls_count:
        if amount == syscalls_count[syscall_name]["amount"]:
            print(f"{syscall_name:<32}"
                  f"{syscalls_count[syscall_name]['archs']}")
