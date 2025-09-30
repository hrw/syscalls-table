import enum
import os
import system_calls
import sys


SYSCALLS = system_calls.syscalls()

class errors(enum.IntEnum):
    NOT_SUPPORTED_SYSTEM_CALL = -1
    NO_SUCH_SYSTEM_CALL = -2


def help():
    print("""usage: syscall [--help|-h] [--dump] syscall arch

Check for Linux system call number/name and availability.

positional arguments:
  syscall     system call number/name
  arch        requested architecture (optional)

options:
  -h, --help  show this help message and exit
  --dump      print all system calls for the given architecture

Examples:
  syscall openat arm64
  syscall 56
  syscall 123 mipso32
  syscall --dump arm64
""")
    sys.exit()


def search_for_syscall_by_number(syscall_number, syscall_arch):
    for syscall_name in SYSCALLS.names():
        try:
            if syscall_number == SYSCALLS.get(syscall_name, syscall_arch):
                return syscall_name
        except system_calls.NotSupportedSystemCall:
            pass
    return None


def search_for_syscalls_by_name(syscall_name, syscall_arch):
    calls = {}
    for name in SYSCALLS.names():
        if syscall_name in name:
            try:
                calls[name] = SYSCALLS.get(name, syscall_arch)
            except system_calls.NotSupportedSystemCall:
                pass
    return calls


def main():
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help"]:
        help()

    syscall_arch = os.uname().machine


    syscalls_list = {}

    if len(sys.argv) == 3:
        syscall_arch = sys.argv[2]

    if syscall_arch not in SYSCALLS.archs():
        if syscall_arch == 'aarch64':
            syscall_arch = 'arm64'
        elif syscall_arch in ['x86-64', 'x64']:
            syscall_arch = 'x86_64'
        else:
            print(f"Architecture {syscall_arch} is not supported.")
            sys.exit(1)

    if sys.argv[1].isnumeric():
        syscall_number = int(sys.argv[1])
        syscall_name = search_for_syscall_by_number(syscall_number,
                                                    syscall_arch)
        if syscall_name:
            syscalls_list[syscall_name] = syscall_number
    else:
        if "--dump" in sys.argv:
            syscall_name = ""
        else:
            syscall_name = sys.argv[1]
        syscalls_list = search_for_syscalls_by_name(syscall_name, syscall_arch)


    if len(syscalls_list):
        for syscall_name in syscalls_list:
            print(f"{syscall_name: <24}\t\t{syscalls_list[syscall_name]}")
    else:
        if syscall_name is None:
            print(f"On {syscall_arch} there is no system call with "
                  f"{syscall_number} number.")
            sys.exit(1)
        else:
            try:
                syscall_number = SYSCALLS.get(syscall_name, syscall_arch)
            except system_calls.NotSupportedSystemCall:
                print(f"System call {syscall_name}() "
                      f"is not supported on {syscall_arch}.")
                sys.exit(1)
            except system_calls.NoSuchSystemCall:
                print(f"There is no such system call as {syscall_name}().")
                sys.exit(1)


if __name__ == '__main__':
    main()
