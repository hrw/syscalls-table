import os

from system_calls.tables.names import syscalls_names
from system_calls.tables.alpha import syscalls_alpha
from system_calls.tables.arc import syscalls_arc
from system_calls.tables.arm64 import syscalls_arm64
from system_calls.tables.armoabi import syscalls_armoabi
from system_calls.tables.arm import syscalls_arm
from system_calls.tables.avr32 import syscalls_avr32
from system_calls.tables.blackfin import syscalls_blackfin
from system_calls.tables.c6x import syscalls_c6x
from system_calls.tables.cris import syscalls_cris
from system_calls.tables.csky import syscalls_csky
from system_calls.tables.frv import syscalls_frv
from system_calls.tables.h8300 import syscalls_h8300
from system_calls.tables.hexagon import syscalls_hexagon
from system_calls.tables.i386 import syscalls_i386
from system_calls.tables.ia64 import syscalls_ia64
from system_calls.tables.m32r import syscalls_m32r
from system_calls.tables.m68k import syscalls_m68k
from system_calls.tables.metag import syscalls_metag
from system_calls.tables.microblaze import syscalls_microblaze
from system_calls.tables.mips64n32 import syscalls_mips64n32
from system_calls.tables.mips64 import syscalls_mips64
from system_calls.tables.mipso32 import syscalls_mipso32
from system_calls.tables.mn10300 import syscalls_mn10300
from system_calls.tables.nds32 import syscalls_nds32
from system_calls.tables.nios2 import syscalls_nios2
from system_calls.tables.openrisc import syscalls_openrisc
from system_calls.tables.parisc import syscalls_parisc
from system_calls.tables.powerpc64 import syscalls_powerpc64
from system_calls.tables.powerpc import syscalls_powerpc
from system_calls.tables.riscv32 import syscalls_riscv32
from system_calls.tables.riscv64 import syscalls_riscv64
from system_calls.tables.s390 import syscalls_s390
from system_calls.tables.s390x import syscalls_s390x
from system_calls.tables.score import syscalls_score
from system_calls.tables.sh64 import syscalls_sh64
from system_calls.tables.sh import syscalls_sh
from system_calls.tables.sparc64 import syscalls_sparc64
from system_calls.tables.sparc import syscalls_sparc
from system_calls.tables.tile64 import syscalls_tile64
from system_calls.tables.tile import syscalls_tile
from system_calls.tables.unicore32 import syscalls_unicore32
from system_calls.tables.x32 import syscalls_x32
from system_calls.tables.x86_64 import syscalls_x86_64
from system_calls.tables.xtensa import syscalls_xtensa


class NoSuchSystemCall(Exception):
    """Exception will be called if asked for not existing system call."""

    pass


class NotSupportedSystemCall(Exception):
    """Exception will be called if asked for system call not supported
    on requested architecture.
    """

    pass


class syscalls(dict):
    def __init__(self):
        self.syscalls = {
            "names": syscalls_names,
            "archs": {
                "alpha": syscalls_alpha,
                "arc": syscalls_arc,
                "arm64": syscalls_arm64,
                "armoabi": syscalls_armoabi,
                "arm": syscalls_arm,
                "avr32": syscalls_avr32,
                "blackfin": syscalls_blackfin,
                "c6x": syscalls_c6x,
                "cris": syscalls_cris,
                "csky": syscalls_csky,
                "frv": syscalls_frv,
                "h8300": syscalls_h8300,
                "hexagon": syscalls_hexagon,
                "i386": syscalls_i386,
                "ia64": syscalls_ia64,
                "m32r": syscalls_m32r,
                "m68k": syscalls_m68k,
                "metag": syscalls_metag,
                "microblaze": syscalls_microblaze,
                "mips64n32": syscalls_mips64n32,
                "mips64": syscalls_mips64,
                "mipso32": syscalls_mipso32,
                "mn10300": syscalls_mn10300,
                "nds32": syscalls_nds32,
                "nios2": syscalls_nios2,
                "openrisc": syscalls_openrisc,
                "parisc": syscalls_parisc,
                "powerpc64": syscalls_powerpc64,
                "powerpc": syscalls_powerpc,
                "riscv32": syscalls_riscv32,
                "riscv64": syscalls_riscv64,
                "s390": syscalls_s390,
                "s390x": syscalls_s390x,
                "score": syscalls_score,
                "sh64": syscalls_sh64,
                "sh": syscalls_sh,
                "sparc64": syscalls_sparc64,
                "sparc": syscalls_sparc,
                "tile64": syscalls_tile64,
                "tile": syscalls_tile,
                "unicore32": syscalls_unicore32,
                "x32": syscalls_x32,
                "x86_64": syscalls_x86_64,
                "xtensa": syscalls_xtensa,
            },
        }

        self.default_arch = os.uname().machine

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
        if arch == "":
            arch = self.default_arch

        try:
            return self.syscalls["archs"][arch][syscall_name]
        except KeyError:
            if syscall_name not in self.syscalls["names"]:
                raise NoSuchSystemCall
            else:
                raise NotSupportedSystemCall

    def archs(self) -> list:
        """Returns list of architectures supported by class.
        Some entries are no longer supported by mainline Linux kernel.
        """
        return list(self.syscalls["archs"].keys())

    def names(self) -> list:
        """Returns list of system calls known by class."""
        return self.syscalls["names"]
