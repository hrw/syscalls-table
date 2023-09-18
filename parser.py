#!/usr/bin/python3

from csv import reader
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from os import listdir
from sys import argv


def load_syscall_data():

    syscalls = {}
    present_archs = []

    # use current system call names - tables/* can contain archive data
    with open("syscall-names.text", newline="") as csvh:
        syscalldata = reader(csvh, delimiter="\t")

        for row in syscalldata:
            syscalls[row[0]] = {}

    for filename in listdir("tables"):

        try:
            arch = filename.replace("syscalls-", "")

            with open(f"tables/{filename}", newline="") as csvh:
                syscalldata = reader(csvh, delimiter="\t")
                present_archs.append(arch)

                for row in syscalldata:
                    try:
                        syscalls[row[0]][arch] = row[1]
                    except KeyError:
                        # old kernel table data - we ignore this syscall
                        pass
                    except IndexError:
                        pass

        except IndexError:
            pass

    return [syscalls, present_archs]


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

    with open("archs-in-kernel", "r") as aikf:
        archs_in_kernel = aikf.read()

    removed_archs = []

    for arch in sorted(present_archs):
        if arch in archs:
            continue
        elif arch in archs_in_kernel:
            archs.append(arch)
        else:
            removed_archs.append(arch)

    for arch in removed_archs:
        archs.append(arch)

    return archs


def generate_html_file():

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

    template = env.get_template('syscalls.html.j2')

    output = template.render(generate_time=datetime.strftime(
                             datetime.utcnow(), "%d %B %Y %H:%M"),
                             archs=archs,
                             kernel_version=kernel_version,
                             syscall_names=sorted(syscalls.keys()),
                             syscall_data=syscalls,
                             minify=True)
    print(output)


if __name__ == "__main__":

    kernel_version = ""

    if len(argv) > 1:
        kernel_version = argv[1]

    [syscalls, present_archs] = load_syscall_data()
    archs = create_arch_list(present_archs)
    generate_html_file()
