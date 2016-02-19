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

import os
import selectors
import subprocess
import sys


def is_program_on_path(prog_name):
    for path in os.get_exec_path():
        if not path or not os.path.isdir(path):
            continue

        if prog_name in os.listdir(path):
            prog_path = os.path.join(path, prog_name)
            if os.access(prog_path, os.X_OK):
                return True
    return False


def transfer_data_file_with_subprocess(subprocess_args):
    process = subprocess.Popen(subprocess_args, bufsize=1,
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)

    output = ""

    def select_callback(stream, mask):
        nonlocal output
        line = stream.readline()
        output += line
        sys.stdout.write(line)

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, select_callback)
    while process.poll() is None:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    return_code = process.wait()
    selector.close()

    success = (return_code == 0)

    return (success, output)
