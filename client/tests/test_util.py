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
from tempfile import NamedTemporaryFile

from client.util import calculate_file_checksum


class TestCalculateFileChecksum(unittest.TestCase):

    def setUp(self):
        self.file_data = "Lorem ipsum dolor sit amet"
        self.correct_md5_checksum = "fea80f2db003d4ebc4536023814aa885"

    def test_md5_checksum(self):
        with NamedTemporaryFile() as f:
            f.write(self.file_data.encode())
            f.flush()
            calculated_checksum = calculate_file_checksum("md5", f.name)
            self.assertEqual(calculated_checksum, self.correct_md5_checksum)
