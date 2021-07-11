"""
Quickly builds a standalone C++ file and runs the result.
"""
import argparse
import shlex
import subprocess
import sys

from pathlib import Path
from tempfile import TemporaryDirectory

DEFAULT_COMPILER = "c++"
DEFAULT_FLAGS = "-Wall -fPIC -std=c++17 -g"


def get_package_flags(package):
    output = subprocess.run(
        ["pkg-config", "--cflags", "--libs", package], capture_output=True
    ).stdout
    return str(output, "utf-8")


def generate_build_script(args):
    build_flags = [DEFAULT_FLAGS]
    if args.flags:
        build_flags.append(args.flags)
    for package in args.packages:
        flags = get_package_flags(package)
        build_flags.append(flags)

    compiler = shlex.quote(args.compiler)
    cpp_file = shlex.quote(args.cpp_file)
    cmd = f"{compiler} {cpp_file} {' '.join(build_flags)}"

    return f"""#!/bin/bash
set -eu
echo "- Building ---------------------"
echo {cmd}
{cmd}
echo "- Running ----------------------"
./a.out
"""


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__
    )

    parser.add_argument(
        "-p",
        "--pkg",
        dest="packages",
        action="append",
        help="pkg-config packages to build with. Any package listed with `pkg-config --list-all` can be used.",
        metavar="PACKAGE",
        default=[],
    )

    parser.add_argument(
        "-l",
        "--live",
        action="store_true",
        help="Automatically rebuild and rerun the executable when the source file changes. Requires the `entr` tool.",
    )

    parser.add_argument(
        "-c",
        "--compiler",
        default=DEFAULT_COMPILER,
        help=f"Compiler to use, instead of {DEFAULT_COMPILER}",
    )

    parser.add_argument(
        "--flags",
        help=f"Compiler flags to use, in addition to the default flags ({DEFAULT_FLAGS})",
    )

    parser.add_argument("cpp_file")

    args = parser.parse_args()

    with TemporaryDirectory(prefix="quickcpp-") as t:
        build_script = Path(t) / "build.sh"
        with open(build_script, "wt") as f:
            script = generate_build_script(args)
            f.write(script)
        build_script.chmod(0o700)

        if args.live:
            try:
                subprocess.run(
                    ["entr", "-c", build_script], input=args.cpp_file.encode("utf-8")
                )
            except FileNotFoundError:
                print(
                    "Can't find the `entr` tool. `entr` is required for live reload.",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            subprocess.run([build_script])
