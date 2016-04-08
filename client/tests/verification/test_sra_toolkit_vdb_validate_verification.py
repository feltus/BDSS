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
from unittest.mock import patch

from client.verification import sra_toolkit_vdb_validate_verification as vdbval_verification


class TestSRAToolkitVDBValidateVerification(unittest.TestCase):

    def test_attempts_verification_only_for_sra_files(self):
        with patch.object(vdbval_verification, "is_program_on_path", return_value=True):
            self.assertTrue(vdbval_verification.can_attempt_verification(None, "/tmp/files/test.sra"))
            self.assertFalse(vdbval_verification.can_attempt_verification(None, "/tmp/files/test.txt"))

    def test_does_not_attempt_verification_if_vdb_validate_not_on_path(self):
        with patch.object(vdbval_verification, "is_program_on_path", return_value=False):
            self.assertFalse(vdbval_verification.can_attempt_verification(None, "/tmp/files/test.sra"))
