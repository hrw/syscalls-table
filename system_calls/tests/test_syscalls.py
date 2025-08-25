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
def test_get_valid_syscall_names(syscall_name, arch, expected_number):
    """Tests for system call names which exist on tested architecture.
    """
    assert syscalls.get(syscall_name, arch) == expected_number


@pytest.mark.parametrize(
    "syscall_number, arch, expected_name",
    [
        (2, "x86_64", "open"),
        (257, "x86_64", "openat"),
        (56, "arm64", "openat"),
        (0, "x86_64", "read"),
        (1, "x86_64", "write"),
        (60, "x86_64", "exit"),
        (458, "riscv64", "listmount"),
    ]
)
def test_get_valid_syscall_numbers(syscall_number, arch, expected_name):
    """Tests for system call numbers which exist on tested architecture.
    """
    assert syscalls.get_name(syscall_number, arch) == expected_name


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("open", "arm64"),
        ("creat", "riscv64"),
    ]
)
def test_unsupported_system_call(syscall_name, arch):
    """Tests for system calls which do not exist on tested architecture.
    """
    with pytest.raises(system_calls.NotSupportedSystemCall):
        syscalls.get(syscall_name, arch)


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("not-existing-system-call", "arm64"),
        ("another-fake-syscall", "x86_64"),
        ("openAT", "arm64"),
        ("openAT", None),
        ("", "arm64"),
        (None, "riscv64"),
        (None, ""),
    ]
)
def test_not_existing_system_call(syscall_name, arch):
    """Tests for system calls which do not exist at all. Including wrong names,
    typos, None, empty string.
    None/empty architecture name is changed in code to host architecture.
    """
    with pytest.raises(system_calls.NoSuchSystemCall):
        syscalls.get(syscall_name, arch)


@pytest.mark.parametrize(
    "syscall_name, arch",
    [
        ("not-existing-system-call", "arm65"),
        ("another-fake-syscall", "x86-64"),
        ("another-fake-syscall", "arm64 "),
    ]
)
def test_no_such_architecture(syscall_name, arch):
    """Tests for wrong architecture names. x86_64 written as x86-64 is an
    error. Spaces are not stripped etc.
    """
    with pytest.raises(system_calls.NoSuchArchitecture):
        syscalls.get(syscall_name, arch)
