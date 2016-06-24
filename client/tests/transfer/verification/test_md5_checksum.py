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

import tempfile
import unittest
from unittest.mock import patch

from client.transfer.base import Transfer, TransferFailedError
from client.transfer.verification import md5_checksum_verification as md5_cv


class TestMD5ChecksumVerification(unittest.TestCase):

    def setUp(self):
        self.file_url = "http://www.example.com/ftp/files/test.sra"
        self.file_data = "hello world"
        self.checksum_url = "http://www.example.com/ftp/files/test.sra.md5"
        self.checksum_data = b"5eb63bbbe01eeed093cb22bb8f5acdc3"
        self.checksum = "5eb63bbbe01eeed093cb22bb8f5acdc3"

        self.transfer = Transfer(self.file_url, "curl", {})

    def test_always_attempts_verification(self):
        self.assertTrue(md5_cv.can_attempt_verification("http://www.example.com/test.txt", None))
        self.assertTrue(md5_cv.can_attempt_verification("https://www.example.com/test.txt", None))
        self.assertTrue(md5_cv.can_attempt_verification("ftp://www.example.com/test.txt", None))
        self.assertTrue(md5_cv.can_attempt_verification("scp://www.example.com:/test.txt", None))

    def test_builds_correct_checksum_url(self):
        self.assertEqual(md5_cv._md5_checksum_url(self.file_url), self.checksum_url)
        self.assertEqual(md5_cv._md5_checksum_url("http://www.example.com/ftp/files/test.sra?param=value#fragment"),
                         "http://www.example.com/ftp/files/test.sra.md5?param=value#fragment")

    def test_get_checksum(self):
        with patch.object(md5_cv.Transfer, "get_data", return_value=self.checksum_data):
            self.assertEqual(md5_cv._get_checksum(self.file_url, "curl", {}), self.checksum)

    def test_validate_checksum(self):
        self.assertTrue(md5_cv._validate_md5_checksum("5eb63bbbe01eeed093cb22bb8f5acdc3"))
        self.assertFalse(md5_cv._validate_md5_checksum("5gb63bbbe01eeed093cb22bb8f5acdc3"))

    def test_correct_checksum_returns_true(self):
        with tempfile.NamedTemporaryFile() as temp_f, patch.object(md5_cv, "_get_checksum", return_value=self.checksum):
            temp_f.write(self.file_data.encode())
            temp_f.flush()
            self.assertTrue(md5_cv.verify_transfer(self.transfer, temp_f.name))

    def test_incorrect_checksum_returns_false(self):
        with tempfile.NamedTemporaryFile() as temp_f, patch.object(md5_cv, "_get_checksum", return_value=self.checksum):
            temp_f.write(self.file_data.encode())
            temp_f.write(b"Corruption")
            temp_f.flush()
            self.assertFalse(md5_cv.verify_transfer(self.transfer, temp_f.name))

    def test_raises_unable_to_verify_if_no_checksum(self):
        with patch.object(md5_cv.Transfer, "get_data", side_effect=TransferFailedError):
            self.assertRaises(TransferFailedError, md5_cv.verify_transfer, self.transfer, None)
