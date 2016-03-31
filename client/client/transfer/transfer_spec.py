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

import selectors
import subprocess
import sys
from collections import namedtuple
from tempfile import NamedTemporaryFile

from .mechanisms import all_mechanisms


class TransferFailedError(Exception):
    pass


TransferSpecBase = namedtuple("TransferSpecBase", "url transfer_mechanism transfer_mechanism_options")


class TransferSpec(TransferSpecBase):

    def transfer_command(self, output_path):
        transfer_module = all_mechanisms[self.transfer_mechanism]
        return transfer_module.transfer_command(self.url, output_path, self.transfer_mechanism_options)

    def run_transfer(self, output_path):
        return _run_in_subprocess(self.transfer_command(output_path))

    def get_transfer_data(self):
        with NamedTemporaryFile() as temp_f:
            success, _ = self.run_transfer(temp_f.name)
            if not success:
                raise TransferFailedError()
            return temp_f.read()


def _run_in_subprocess(subprocess_args, successful_return_codes=(0,)):
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

    success = return_code in successful_return_codes

    return (success, output)
