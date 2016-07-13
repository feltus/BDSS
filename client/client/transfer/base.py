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

from .mechanisms import default_mechanism, get_mechanism


logger = logging.getLogger("bdss")


class TransferFailedError(Exception):
    pass


_user_options_cache = {}


class Transfer():

    def __init__(self, url=None, mechanism_name=None, mechanism_options=None, data_source_id=None):
        """

        Parameters:
        url - String -
        mechanism_name - String -
        mechanism_options - dict -
        data_source_id - String - If provided, user options will be cached such that multiple transfers
            from the same data source only prompt the first time.
        """
        self.url = url
        self.mechanism_name = mechanism_name
        self.mechanism_options = mechanism_options
        if url and not mechanism_name:
            (self.mechanism_name, self.mechanism_options) = default_mechanism(url)
        if not self.mechanism_options:
            self.mechanism_options = {}
        self.data_source_id = str(data_source_id)

        self.mechanism = get_mechanism(self.mechanism_name, self.mechanism_options)

        try:
            self.mechanism_user_opts = _user_options_cache[self.data_source_id]
        except KeyError:
            self.mechanism_user_opts = self.mechanism.prompt_for_user_input_options()
            if self.data_source_id:
                _user_options_cache[self.data_source_id] = self.mechanism_user_opts

        self.mechanism.update_options(self.mechanism_user_opts)

    def run(self, output_path, display_output=True):
        """
        Run transfer.

        Parameters:
        output_path - String - The path to save the transferred file to.
        display_output - Boolean - Display mechanism output as transfer runs.

        Returns:
        (Boolean, String) - Tuple of (True/False for success/failure, Mechanism output)
        """
        return self.mechanism.transfer_file(self.url, output_path, display_output)

    def get_data(self, display_output=True):
        """
        Run transfer to temporary file. Return contents and delete temp file.

        Parameters:
        display_output - Boolean - Display mechanism output as transfer runs.
        """
        with NamedTemporaryFile() as temp_f:
            (success, _) = self.run(temp_f.name, display_output)
            if not success:
                raise TransferFailedError
            return temp_f.read()

    def __eq__(self, other):
        return (self.url == other.url and
                self.mechanism_name == other.mechanism_name and
                self.mechanism_options == other.mechanism_options and
                self.mechanism_user_opts == other.mechanism_user_opts)

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
