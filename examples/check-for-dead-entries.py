#!/usr/bin/python3

"""
Check for system calls which are not present on any architecture.
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

for syscall_name in syscalls_count:
    if 0 == syscalls_count[syscall_name]["amount"]:
        print(f"{syscall_name:<32}")
