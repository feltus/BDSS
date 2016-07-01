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

import hashlib
import io
import os
import selectors
import subprocess
import sys


def calculate_file_checksum(algorithm, path, blocksize=65536):
    """
    Calculate the checksum of the file at path using the given algorithm.
    See hashlib.available_algorithms
    https://docs.python.org/3/library/hashlib.html
    """
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            h.update(block)
    return h.hexdigest().lower()


def is_program_on_path(prog_name):
    """
    Check if a program is found on the executable search path.

    Parameters:
    prog_name - String - Name of the program

    Returns:
    Boolean - True if program is found
    """
    for path in os.get_exec_path():
        if not path or not os.path.isdir(path):
            continue

        if prog_name in os.listdir(path):
            prog_path = os.path.join(path, prog_name)
            if os.access(prog_path, os.X_OK):
                return True

    return False


def run_subprocess(subprocess_args, display_output=True):
    """
    Run a program in a subprocess. Display and capture output.

    Parameters:
    subprocess_args - String[] - Args to subprocess.Popen. See https://docs.python.org/3/library/subprocess.html#popen-constructor
    display_output - Boolean - Display output of subprocess as it runs.

    Returns:
    (Boolean, String) - Tuple of Boolean true/false if subprocess succeeded/failed based on given return codes and
    String containing output of subprocess.
    """
    process = subprocess.Popen(subprocess_args,
                               bufsize=1,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)

    buf = io.StringIO()

    def select_callback(stream, mask):
        line = stream.readline()
        buf.write(line)
        if display_output:
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

    output = buf.getvalue()
    buf.close()

    return (return_code == 0, output)
