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

from client.transfer import mechanisms


class TestDefaultMechanism(unittest.TestCase):

    def test_correct_default_mechanism_for_url_scheme(self):

        self.assertEqual(mechanisms.default_mechanism("http://example.com/file.txt")[0], "curl")
        self.assertEqual(mechanisms.default_mechanism("https://example.com/file.txt")[0], "curl")
        self.assertEqual(mechanisms.default_mechanism("ftp://example.com/file.txt")[0], "curl")

        self.assertEqual(mechanisms.default_mechanism("scp://user@example.com:/file.txt")[0], "scp")

        self.assertEqual(mechanisms.default_mechanism("sshftp://user@example.com/file.txt")[0], "gridftp_lite")

        self.assertEqual(mechanisms.default_mechanism("aspera://example.com:/file.txt")[0], "aspera")
