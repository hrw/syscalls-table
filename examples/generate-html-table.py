#!/usr/bin/python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import system_calls
from system_calls import architectures_in_kernel


def create_arch_list(present_archs):

    # the main ones go first
    archs = [
        "arm64",
        "arm",
        "armoabi",
        "x86_64",
        "x32",
        "i386",
        "powerpc64",
        "powerpc",
        "s390x",
        "s390",
    ]

    removed_archs = []

    for arch in sorted(present_archs):
        if arch in archs:
            continue
        elif arch in architectures_in_kernel.architectures:
            archs.append(arch)
        else:
            removed_archs.append(arch)

    for arch in removed_archs:
        archs.append(arch)

    return archs


def generate_system_calls_tree():

    syscalls_for_template = {}

    for syscall_name in syscalls.names():
        syscalls_for_template[syscall_name] = {}

        for arch in syscalls.archs():
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

    output = template.render(generate_time=datetime.strftime(
                             datetime.utcnow(), "%d %B %Y %H:%M"),
                             archs=create_arch_list(syscalls.archs()),
                             syscalls=generate_system_calls_tree(),
                             syscall_names=syscalls.names(),
                             minify=True)
    print(output)


syscalls = system_calls.syscalls()
generate_html_file()
