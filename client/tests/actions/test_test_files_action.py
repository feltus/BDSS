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
from urllib.parse import urljoin

import requests_mock

from client.actions import test_files_action
from client.config import metadata_repository_url


class TestTestFilesAction(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_test_files(self, m):
        m.get(urljoin(metadata_repository_url, "data_sources/1/test_files"),
              json={"test_files": ["a", "b", "c"]},
              status_code=200)

        self.assertEqual(test_files_action.get_test_files(1), ["a", "b", "c"])

    @requests_mock.Mocker()
    @patch.object(test_files_action.logger, "warn")
    def test_nonexistent_data_source(self, m, warn):
        m.get(urljoin(metadata_repository_url, "data_sources/2/test_files"), status_code=404)

        self.assertEqual(test_files_action.get_test_files(2), [])
        self.assertTrue(warn.called)

    @requests_mock.Mocker()
    def test_server_error(self, m):
        m.get(urljoin(metadata_repository_url, "data_sources/3/test_files"), status_code=500)

        self.assertRaises(Exception, test_files_action.get_test_files, 3)
