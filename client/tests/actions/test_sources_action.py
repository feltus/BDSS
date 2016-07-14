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
from urllib.parse import urljoin

import requests_mock

from client.actions import sources_action
from client.config import metadata_repository_url


class TestSourcesAction(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_matching_sources(self, m):

        mock_sources = [
            {"id": 1, "label": "source a"},
            {"id": 2, "label": "source b"},
            {"id": 3, "label": "source c"},
        ]

        m.get(urljoin(metadata_repository_url, "data_sources/search?q=source"),
              json={"data_sources": mock_sources},
              status_code=200)

        self.assertEqual(sources_action.get_matching_data_sources("source"), mock_sources)
