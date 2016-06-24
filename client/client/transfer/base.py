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

import logging
import textwrap

from tempfile import NamedTemporaryFile

from .mechanisms import all_mechanisms, default_mechanism


logger = logging.getLogger("bdss")


class TransferFailedError(Exception):
    pass


class Transfer():

    def __init__(self, url=None, mechanism_name=None, mechanism_options=None):
        self.url = url
        self.mechanism_name = mechanism_name
        self.mechanism_options = mechanism_options
        if url and not mechanism_name:
            (self.mechanism_name, self.mechanism_options) = default_mechanism(url)

    @property
    def mechanism(self):
        mechanism_class = all_mechanisms[self.mechanism_name]
        opts = self.mechanism_options if self.mechanism_options else {}
        return mechanism_class(**opts)

    def run(self, output_path):
        """
        Run transfer.

        Parameters:
        output_path - String - The path to save the transferred file to.

        Returns:
        (Boolean, String) - Tuple of (True/False for success/failure, Mechanism output)
        """
        return self.mechanism.transfer_file(self.url, output_path)

    def get_data(self):
        """
        Run transfer to temporary file. Return contents and delete temp file.
        """
        with NamedTemporaryFile() as temp_f:
            (success, _) = self.run(temp_f.name)
            if not success:
                raise TransferFailedError
            return temp_f.read()

    def __str__(self):
        return textwrap.dedent("""\
            Transfer:
            URL = %s
            mechanism = %s
            %s""" % (
            self.url,
            self.mechanism_name,
            "\n".join(["   %s: %s" % (k, v) for k, v in self.mechanism_options.items()]) if self.mechanism_options else "   No options"
        ))
