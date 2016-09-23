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

from getpass import getpass

from voluptuous import Invalid, Required, Schema

from ...util import is_program_on_path, run_subprocess


class UserInputOption():

    def __init__(self, key, prompt=None, validation=str, hide_input=False):
        self.key = key
        self.prompt = prompt
        if not self.prompt:
            self.prompt = "%s? " % self.key
        self.validation = validation
        self.hide_input = hide_input

    def prompt_for_value(self):
        validate = Schema({Required("value"): self.validation})
        value_valid = False
        value = None
        while not value_valid:
            try:
                if self.hide_input:
                    value = getpass(self.prompt)
                else:
                    value = input(self.prompt)
                validate({"value": value})
                value_valid = True
            except Invalid as e:
                print("Invalid input:", e.msg)

        return value


class BaseMechanism():

    @classmethod
    def allowed_options(self):
        """
        List of option names to filter options passed from metadata repository against.

        Returns:
        String[] - Names of options to allow.
        """
        return []

    def __init__(self, **kwargs):

        # Initialize all allowed options
        for opt in self.__class__.allowed_options():
            setattr(self, opt, None)

        # Set passed options
        self.update_options(kwargs)

    @classmethod
    def is_available(cls):
        """
        Determine if the transfer mechanism is available on this machine.
        Usually involves checking if a specific program is found on the PATH.

        Returns:
        Boolean - True if available
        """
        raise NotImplementedError

    def transfer_file(self, url, partial_range, output_path, display_output=True):
        """
        Transfer a file.

        Parameters:
        url - String - URL of the file to transfer
        partial_range - tuple (int, int) - Partial section of file to transfer. First number is offset from start,
            second number is length of partial transfer. If None, transfer the entire file.
        output_path - String - Path to write transferred file to
        display_output - Boolean - Output progress information

        Returns:
        (Boolean, String) - Tuple of (True/False for success/failure, Mechanism output)
        """
        raise NotImplementedError

    def user_input_options(self):
        """
        Define options whose values must be supplied by the end user.

        Returns:
        UserInputOption[]
        """
        return []

    def prompt_for_user_input_options(self):
        """
        Prompt the user for additional options for this mechanism.
        The available options are preconfigured with the `user_input_options` method.

        Returns:
        dict - Items are key and value of options.
        """
        opts = {}
        for opt in self.user_input_options():
            opts[opt.key] = opt.prompt_for_value()
        return opts

    def update_options(self, opts):
        """
        Store options as attributes on this mechanism.

        Parameters:
        opts - dict - Options. Keys and values will correspond to attribute names and values.
        """
        for opt, val in opts.items():
            if opt not in self.__class__.allowed_options():
                raise AttributeError("%s does not support a '%s' option" % (self.__class__.__name__, opt))
            else:
                setattr(self, opt, val)


class SimpleSubprocessMechanism(BaseMechanism):

    @classmethod
    def is_available(cls):
        return is_program_on_path(cls.transfer_program())

    @classmethod
    def transfer_program(cls):
        raise NotImplementedError

    def transfer_file(self, url, partial_range, output_path, display_output=True):
        return run_subprocess(self.transfer_command(url, partial_range, output_path), display_output)

    def transfer_command(self, url, partial_range, output_path):
        raise NotImplementedError
