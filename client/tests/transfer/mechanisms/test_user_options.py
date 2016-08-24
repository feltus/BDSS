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
from unittest.mock import call, patch

from voluptuous import All, Range

from client.transfer.mechanisms import base


class TestUserInputOptionMechanism(unittest.TestCase):

    @patch("builtins.input", return_value="Hello")
    def test_user_input_option_prompts(self, mock_input):
        opt = base.UserInputOption("option", "Option value?")
        val = opt.prompt_for_value()
        mock_input.assert_called_once_with("Option value?")
        self.assertEqual(val, "Hello")

    @patch.object(base, "getpass", return_value="World")
    @patch("builtins.input", return_value="Hello")
    def test_user_input_option_prompts_with_hidden_input(self, mock_input, mock_getpass):
        opt = base.UserInputOption("option", "Option value?", hide_input=True)
        val = opt.prompt_for_value()
        mock_getpass.assert_called_once_with("Option value?")
        self.assertEqual(val, "World")

    @patch("builtins.input", side_effect=["a", -1, 5])
    def test_prompt_until_valid_value(self, mock_input):
        opt = base.UserInputOption("option", "Option value?", validation=All(int, Range(min=4, max=8)))
        val = opt.prompt_for_value()
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(val, 5)
