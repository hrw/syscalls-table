import importlib
import os

from system_calls.tables.names import syscalls_names
from system_calls.linux_version import linux_version


class NoSuchSystemCall(Exception):
    """Exception will be called if asked for not existing system call."""

    pass


class NotSupportedSystemCall(Exception):
    """Exception will be called if asked for system call not supported
    on requested architecture.
    """

    pass


class NoSuchArchitecture(Exception):
    """Exception will be called if asked for system call for not supported
    architecture.
    """

    pass


class syscalls:
    def __init__(self):
        self._archs = [
            "alpha", "arc", "arm64", "armoabi", "arm", "avr32", "blackfin",
            "c6x", "cris", "csky", "frv", "h8300", "hexagon", "i386", "ia64",
            "loongarch64", "m32r", "m68k", "metag", "microblaze", "mips64n32",
            "mips64", "mipso32", "mn10300", "nds32", "nios2", "openrisc",
            "parisc", "powerpc64", "powerpc", "riscv32", "riscv64", "s390",
            "s390x", "score", "sh64", "sh", "sparc64", "sparc", "tile64",
            "tile", "unicore32", "x32", "x86_64", "xtensa"
        ]

        self._names = syscalls_names
        self._default_arch = os.uname().machine
        if self._default_arch == 'aarch64':
            self._default_arch = 'arm64'

        self._loaded_arch_tables = {}
        self._names = syscalls_names
        self.linux_version = linux_version

    def load_arch_table(self, arch: str):
        """Loads an architecture table dynamically."""
        if arch not in self._loaded_arch_tables:
            if arch not in self._archs:
                raise NoSuchArchitecture
            try:
                module_name = f"system_calls.tables.{arch}"
                module = importlib.import_module(module_name)
                table = getattr(module, f"syscalls_{arch}")
                self._loaded_arch_tables[arch] = table
            except (ImportError, AttributeError) as e:
                # Handle cases where module/table might be missing/malformed
                raise RuntimeError("Failed to load table for architecture "
                                   f"'{arch}': {e}") from e
        return self._loaded_arch_tables[arch]

    def __getitem__(self, syscall_name: str) -> int:
        """Returns number for requested system call.
        Host architecture would be used.
        """
        return self.get(syscall_name)

    def get(self, syscall_name: str, arch: str = "") -> int:  # type: ignore
        """Returns number for requested system call.
        Architecture can be provided by second argument (optional, host
        architecture would be used by default).
        """
        if arch == "" or arch is None:
            arch = self._default_arch

        # First, try to load/get the architecture's table
        try:
            arch_table = self.load_arch_table(arch)
        except NoSuchArchitecture:
            raise NoSuchArchitecture

        try:
            return arch_table[syscall_name]
        except KeyError:
            if syscall_name not in self._names:
                raise NoSuchSystemCall
            else:
                raise NotSupportedSystemCall

    def archs(self) -> list:
        """Returns list of architectures supported by class.
        Some entries are no longer supported by mainline Linux kernel.
        """
        return self._archs

    def names(self) -> list:
        """Returns list of system calls known by class."""
        return self._names
