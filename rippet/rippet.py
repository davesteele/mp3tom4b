#!/usr/bin/python3
# Copyright (c) 2018 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-3
# License-Filename: LICENSE

import subprocess
import shlex
import argparse


def do_rip(disk_num):
    file_fmt = "Disk%(album_number)2.2dTrack%(track_number)2.2d.mp3"
    cmd = f"cdda2track -t mp3 --album-number {disk_num} --format=\"{file_fmt}\""
    subprocess.call(shlex.split(cmd))


def process_args():
    parser = argparse.ArgumentParser(
        description="Parse a CD to sortable tracks",
    )

    parser.add_argument(
        "disk_number",
        type=int,
        help="disk number",
    )

    args = parser.parse_args()

    return args


def main():
    args = process_args()

    do_rip(args.disk_number)


if __name__ == "__main__":
    main()
