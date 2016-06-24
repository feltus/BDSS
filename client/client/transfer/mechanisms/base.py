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

from ...util import is_program_on_path, run_subprocess


class BaseMechanism():

    @classmethod
    def allowed_options(self):
        return []

    def __init__(self, **kwargs):

        # Initialize all allowed options
        for opt in self.__class__.allowed_options():
            setattr(self, opt, None)

        # Set passed options, validate against allowed options
        for opt, val in kwargs.items():
            if opt not in self.__class__.allowed_options():
                raise AttributeError("%s does not support a '%s' option" % (self.__class__.__name__, opt))
            else:
                setattr(self, opt, val)

    @classmethod
    def is_available(cls):
        """
        Determine if the transfer mechanism is available on this machine.

        Returns:
        Boolean - True if available
        """
        raise NotImplementedError

    def transfer_file(self, url, output_path):
        """
        Transfer a file.

        Parameters:
        url - String - URL of the file to transfer
        output_path - String - Path to write transferred file to

        Returns:
        (Boolean, String) - Tuple of (True/False for success/failure, Mechanism output)
        """
        raise NotImplementedError


class SimpleSubprocessMechanism(BaseMechanism):

    @classmethod
    def is_available(cls):
        return is_program_on_path(cls.transfer_program())

    @classmethod
    def transfer_program(cls):
        raise NotImplementedError

    def transfer_file(self, url, output_path):
        return run_subprocess(self.transfer_command(url, output_path))

    def transfer_command(self, url, output_path):
        raise NotImplementedError
