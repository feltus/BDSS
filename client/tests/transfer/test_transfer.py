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

import unittest
from unittest.mock import ANY, call, patch

from client.transfer import base as transfer_base
from client.transfer.mechanisms.base import BaseMechanism, UserInputOption


class MockMechanism(BaseMechanism):

    @classmethod
    def allowed_options(cls):
        return ("test_opt",)

    @classmethod
    def is_available(cls):
        return True

    def transfer_file(self, url, output_path):
        return (True, "")

    def user_input_options(self):
        return [UserInputOption("test_opt", "Value for option?")]


class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.file_url = "http://www.example.com/files/test.txt"
        self.transfer_mechanism = "curl"
        self.transfer_mechanism_options = {}
        self.output_path = "/tmp/test.txt"
        self.file_data = b"hello world"

    def _write_file_data(self, output_path):
        with open(output_path, "w+b") as f:
            f.write(self.file_data)
        return (True, "")

    def test_get_transfer_data(self):
        transfer = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options)
        with patch.object(transfer, "run", side_effect=self._write_file_data) as mock_run_transfer:
            data = transfer.get_data()
            mock_run_transfer.assert_called_once_with(ANY)
            self.assertEqual(data, self.file_data)

    def test_raises_if_unable_to_transfer(self):
        """
        Transfer#get_transfer_data should raise a TransferFailedError if run_transfer reported failure.
        """
        transfer = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options)
        with patch.object(transfer, "run", return_value=(False, "")):
            self.assertRaises(transfer_base.TransferFailedError, transfer.get_data)

    @patch.object(transfer_base, "get_mechanism", side_effect=lambda m, o: MockMechanism())
    @patch("builtins.input", return_value="Hello")
    def test_user_options_cache(self, mock_input, mock_get_mechanism):
        # First transfer for this data source should prompt
        transferOne = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options, data_source_id=1)
        mock_input.assert_called_once_with("Value for option?")
        self.assertEqual(transferOne.mechanism.test_opt, "Hello")

        # Second should use cached value
        transferTwo = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options, data_source_id=1)
        mock_input.assert_called_once_with("Value for option?")
        self.assertEqual(transferTwo.mechanism.test_opt, "Hello")

    @patch.object(transfer_base, "get_mechanism", side_effect=lambda m, o: MockMechanism())
    @patch("builtins.input", return_value="Hello")
    def test_unknown_data_sources_do_not_cache_user_options(self, mock_input, mock_get_mechanism):
        # Transfers without a known data source should not cache options
        transferOne = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options)
        mock_input.assert_called_once_with("Value for option?")
        self.assertEqual(transferOne.mechanism.test_opt, "Hello")

        transferTwo = transfer_base.Transfer(self.file_url, self.transfer_mechanism, self.transfer_mechanism_options)
        self.assertEqual(mock_input.call_args_list, [call("Value for option?"), call("Value for option?")])
        self.assertEqual(transferTwo.mechanism.test_opt, "Hello")
