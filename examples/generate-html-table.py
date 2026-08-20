#!/usr/bin/python3

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader

import system_calls
from system_calls import architectures_in_kernel


def create_arch_list():

    # the main ones go first
    archs = [
        "arm64",
        "arm",
        "armoabi",
        "x86_64",
        "x32",
        "i386",
        "riscv64",
        "riscv32",
        "powerpc64",
        "powerpc",
        "s390x",
    ]

    removed_archs = []

    for arch in sorted(architectures_in_kernel.architectures):
        if arch in archs:
            continue
        else:
            archs.append(arch)

    for arch in syscalls.removed_archs():
        archs.append(arch)

    return archs


def generate_system_calls_tree():

    syscalls_for_template = {
        'linux_version': system_calls.linux_version
    }

    archs = syscalls.archs()

    for syscall_name in syscalls.names():
        syscalls_for_template[syscall_name] = {}

        for arch in archs:
            try:
                syscalls_for_template[syscall_name][arch] = (
                    syscalls.get(syscall_name, arch))
            except system_calls.NotSupportedSystemCall:
                syscalls_for_template[syscall_name][arch] = -1

    return syscalls_for_template


def generate_html_file():

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

    template = env.get_template('syscalls.html.j2')

    archs = create_arch_list()

    output = template.render(generate_time=datetime.strftime(
                             datetime.now(timezone.utc), "%d %B %Y %H:%M"),
                             archs=archs,
                             hide_removed_archs=list(
                                 range(len(archs) -
                                       len(syscalls.removed_archs()) + 1,
                                       len(archs) + 1)),
                             hide_all_archs=list(range(1, len(archs) + 1)),
                             syscalls=generate_system_calls_tree(),
                             syscall_names=syscalls.names(),
                             git_repo="syscalls-table",
                             extra_build_info=" using data from "
                             f"{ system_calls.linux_version } "
                             "kernel source",
                             minify=True)
    print(output)


syscalls = system_calls.syscalls()
generate_html_file()
