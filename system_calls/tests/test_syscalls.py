#!/usr/bin/env python3

import pytest
import system_calls

syscalls = system_calls.syscalls()


@pytest.mark.parametrize(
    "syscall_name, arch, expected_number",
    [
        ("open", "x86_64", 2),
        ("openat", "x86_64", 257),
        ("openat", "arm64", 56),
        ("read", "x86_64", 0),
        ("write", "x86_64", 1),
        ("exit", "x86_64", 60),
        ("listmount", "riscv64", 458),
    ]
)
def test_get_valid_syscalls(syscall_name, arch, expected_number):
    assert syscalls.get(syscall_name, arch) == expected_number


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("open", "arm64"),
        ("creat", "riscv64"),
    ]
)
def test_unsupported_system_call(syscall_name, arch):
    with pytest.raises(system_calls.NotSupportedSystemCall):
        syscalls.get(syscall_name, arch)


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("not-existing-system-call", "arm64"),
        ("another-fake-syscall", "x86_64"),
    ]
)
def test_not_existing_system_call(syscall_name, arch):
    with pytest.raises(system_calls.NoSuchSystemCall):
        syscalls.get(syscall_name, arch)


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("not-existing-system-call", "arm65"),
        ("another-fake-syscall", "x86-64"),
    ]
)
def test_no_such_architecture(syscall_name, arch):
    with pytest.raises(system_calls.NoSuchArchitecture):
        syscalls.get(syscall_name, arch)
