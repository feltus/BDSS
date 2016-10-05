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

import json
import os

from .base import BaseTestCase

from app.routes.configuration import load_configuration


class TestDataSourceSearch(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client as c:
            self.loginTestUser()
            test_conf_path = os.path.join(os.path.dirname(__file__), "../test_config.json")
            test_conf = open(test_conf_path).read()
            load_configuration(test_conf)
            c.get("/logout")

    def test_no_query_html_returns_form(self):
        with self.client as c:
            r = c.get("/data_sources/search")
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"Search Results", r.data)
            self.assertRegex(r.get_data(as_text=True), r"<form.*?action=\"\/data_sources\/search\".*?>")

    def test_query_html_results(self):
        with self.client as c:
            r = c.get("/data_sources/search?q=ftp")
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"Search Results", r.data)
            self.assertRegex(r.get_data(as_text=True), r"<form.*?action=\"\/data_sources\/search\".*?>")
            self.assertIn(b"Example FTP", r.data)

    def test_no_query_json_returns_400(self):
        with self.client as c:
            r = c.get("/data_sources/search", headers=dict(Accept="application/json"))
            self.assertEqual(r.status_code, 400)

    def test_query_json_results(self):
        with self.client as c:
            r = c.get("/data_sources/search?q=example", headers=dict(Accept="application/json"))
            results = json.loads(r.get_data(as_text=True))
            source_labels = [s["label"] for s in results["data_sources"]]
            self.assertEqual(r.status_code, 200)
            self.assertIn("Example FTP", source_labels)
            self.assertIn("Example HTTP", source_labels)
