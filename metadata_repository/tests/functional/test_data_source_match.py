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

import os

from .base import BaseTestCase

from app.models import DataSource
from app.routes.configuration import load_configuration


class TestDataSourceMatch(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client as c:
            self.loginTestUser()
            test_conf_path = os.path.join(os.path.dirname(__file__), "../test_config.json")
            test_conf = open(test_conf_path).read()
            load_configuration(test_conf)

            ds = DataSource(id=4, label="Test Source", transfer_mechanism_type="curl")
            self.addToDatabase(ds)

            self.ftp_source_id = DataSource.query.filter(DataSource.label == "Example FTP").first().id

            c.get("/logout")

    def test_get_form(self):
        with self.client as c:
            self.loginTestUser()
            r = c.get("/data_sources/%d/test_match" % self.ftp_source_id)
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"Test URL Match", r.data)
            self.assertRegex(r.get_data(as_text=True), r"<form.*?action=\"\/data_sources\/1\/test_match\".*?>")

    def test_source_has_no_matchers(self):
        with self.client as c:
            self.loginTestUser()
            r = c.get("/data_sources/4/test_match")
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"Test URL Match", r.data)
            self.assertNotIn(b"<form", r.data)
            self.assertIn(b"This data source has no URL matchers", r.data)

    def test_matching_url(self):
        with self.client as c:
            self.loginTestUser()
            r = c.post("/data_sources/%d/test_match" % self.ftp_source_id,
                       data=dict(url="ftp://example.com/file.txt"))
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"URL matches", r.data)

    def test_nonmatching_urls(self):
        with self.client as c:
            self.loginTestUser()
            r = c.post("/data_sources/%d/test_match" % self.ftp_source_id,
                       data=dict(url="http://example.com/file.txt"))
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"URL does not match", r.data)

            r = c.post("/data_sources/%d/test_match" % self.ftp_source_id,
                       data=dict(url="ftp://example.org/file.txt"))
            self.assertEqual(r.status_code, 200)
            self.assertIn(b"URL does not match", r.data)
