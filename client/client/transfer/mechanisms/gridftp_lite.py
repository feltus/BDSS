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

from .base import SimpleSubprocessMechanism


class GridFTPLiteMechanism(SimpleSubprocessMechanism):

    @classmethod
    def allowed_options(cls):
        return (
            "fast_mode",
            "parallelism",
            "block_size",
            "tcp_buffer_size"
        )

    @classmethod
    def transfer_program(cls):
        return "globus-url-copy"

    def transfer_command(self, url, partial_range, output_path):
        args = []

        try:
            if self.fast_mode:
                args.append("-fast")
        except KeyError:
            pass

        try:
            if self.parallelism:
                args.extend(["-p", str(self.parallelism)])
        except KeyError:
            pass

        try:
            if self.block_size:
                args.extend(["-block-size", str(self.block_size)])
        except KeyError:
            pass

        try:
            if self.tcp_buffer_size:
                args.extend(["-tcp-buffer-size", str(self.tcp_buffer_size)])
        except KeyError:
            pass

        if partial_range:
            args.extend([
                "-partial-offset", partial_range[0],
                "-partial-length", partial_range[1]
            ])

        return ["globus-url-copy"] + args + [url, output_path]
