# What is it?

This is very simple code to get system call number/name and availability from
Python level.

## What and why?

Linux kernel has set of system calls (called syscalls in short) offered for
userspace. Each architecture can support them but the numbers used for their
identification can vary between archs.

And those numbers are important for several projects (like Valgrind for
example).


# Usage in Python

Please check "bin/syscall" script and files in "examples/" directory.


# Packages

## Pypi

Package is available on Pypi so `pip install system-calls` should work.

## Fedora

Package for rawhide is available in distribution repositories.

## Other distributions

I do not plan to work on packaging for other distributions.


# How to help?

Check issues list and work on any of them.


# Where to see HTML table?

I keep copy at https://marcin.juszkiewicz.com.pl/download/tables/syscalls.html
page.


# Why syscalls-table looks like python-syscalls now?

I needed to merge both projects to make it more manageable. Now all data is
kept in one place so I do not need to synchronize it between projects.

The plan is to have some kind of CI which would handle updates. Probably not
via GitHub Actions but something on my personal server (easier to copy HTML
table to server).
