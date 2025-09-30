#!/usr/bin/python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="system-calls",
    version="6.17.0",
    author="Marcin Juszkiewicz",
    author_email="marcin-python@juszkiewicz.com.pl",
    description="Python module to check for system call number/name and"
    "availability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hrw/syscalls-table",
    project_urls={
        "Bug Tracker": "https://github.com/hrw/syscalls-table/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=["system_calls", "system_calls/tables/", "system_calls/tests/"],
    python_requires=">=3.6",
    license_files=["LICENSE"],
    entry_points={'console_scripts': ["syscall = system_calls.cli:main"]},
    data_files=[("share/man/man1", ["man/syscall.1"])],
    install_requires=['jinja2'],
)
