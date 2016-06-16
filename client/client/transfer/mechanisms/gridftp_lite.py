# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from ...util import is_program_on_path


def is_available():
    return is_program_on_path("globus-url-copy")


def transfer_command(url, output_path, options):
    args = []

    try:
        if options["fast_mode"]:
            args.append("-fast")
    except KeyError:
        pass

    try:
        if options["parallelism"]:
            args.extend(["-p", int(options["parallelism"])])
    except KeyError:
        pass

    try:
        if options["block_size"]:
            args.extend(["-block-size", int(options["block_size"])])
    except KeyError:
        pass

    try:
        if options["tcp_buffer_size"]:
            args.extend(["-tcp-buffer-size", int(options["tcp_buffer_size"])])
    except KeyError:
        pass

    return ["globus-url-copy"] + args + [url, output_path]
