#!/usr/bin/env python3

import pytest
import system_calls

syscalls = system_calls.syscalls()


def test_x86_64_open():
    assert 2 == syscalls.get("open", "x86_64")


def test_x86_64_openat():
    assert 257 == syscalls.get("openat", "x86_64")


def test_arm64_openat():
    assert 56 == syscalls.get("openat", "arm64")


def test_on_arm64_open_is_not_supported():
    with pytest.raises(system_calls.NotSupportedSystemCall):
        print(syscalls.get("open", "arm64"))


def test_not_existing_system_call():
    with pytest.raises(system_calls.NoSuchSystemCall):
        print(syscalls.get("not-existing-system-call", "arm64"))
