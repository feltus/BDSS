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

from client.actions import transfer_action
from client.config import metadata_repository_url


class TestTransferAction(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_transfers(self, m):

        mock_transfers = [
            {"url": "http://example.com/test.txt", "mechanism_name": "curl", "mechanism_options": {}}
        ]

        m.post(urljoin(metadata_repository_url, "transfers"),
               json={"transfers": mock_transfers},
               status_code=200)

        self.assertEqual(len(transfer_action.get_transfers("http://example.com/test.txt", ["curl"])), 1)

    @requests_mock.Mocker()
    @patch.object(transfer_action.logger, "warn")
    def test_get_transfers_appends_default_transfer_if_no_transfers(self, m, warn):

        mock_transfers = []

        m.post(urljoin(metadata_repository_url, "transfers"),
               json={"transfers": mock_transfers},
               status_code=200)

        self.assertEqual(len(transfer_action.get_transfers("http://example.com/test.txt", ["curl"])), 1)
        self.assertTrue(warn.called)

    @requests_mock.Mocker()
    @patch.object(transfer_action.logger, "warn")
    def test_get_transfers_returns_default_transfer_if_request_fails(self, m, warn):

        m.post(urljoin(metadata_repository_url, "transfers"),
               status_code=500)

        self.assertEqual(len(transfer_action.get_transfers("http://example.com/test.txt", ["curl"])), 1)
        self.assertTrue(warn.called)

    @requests_mock.Mocker()
    def test_get_transfers_appends_default_transfer_if_not_present(self, m):

        mock_transfers = [
            {"url": "http://example.com/test.txt", "mechanism_name": "aspera", "mechanism_options": {}}
        ]

        m.post(urljoin(metadata_repository_url, "transfers"),
               json={"transfers": mock_transfers},
               status_code=200)

        self.assertEqual(len(transfer_action.get_transfers("http://example.com/test.txt", ["curl", "aspera"])), 2)
