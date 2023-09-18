# System calls table on different architectures

## What and why?

Linux kernel has a set of system calls (called syscalls in short) offered for userspace.
Each architecture can support them but the numbers used for their identification
can vary between archs.

And those numbers can be important for some projects (like Valgrind for example).

## How to help?

Check issues list and work on any of them.

## Where to see HTML table?

I keep a copy at https://marcin.juszkiewicz.com.pl/download/tables/syscalls.html page.


## Python support

As a part of this project I provide code to get system call number/name and
availability from Python level.

### Usage

Please check "bin/syscall" script and files in "examples/" directory.


## Why this project looks like python-syscalls one?

I needed to merge both projects to make it more manageable. Now all data is
kept in one place so I do not need to synchronize it between projects.

The plan is to have some kind of CI which would handle updates.
