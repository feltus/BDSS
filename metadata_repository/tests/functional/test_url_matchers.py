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

from .base import BaseTestCase

from app.models import DataSource, UrlMatcher


class TestUrlMatchers(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client:
            self.loginTestUser()

            ds = DataSource(id=1,
                            label="Test Source",
                            transfer_mechanism_type="curl")
            matcher = UrlMatcher(data_source_id=1,
                                 matcher_id=1,
                                 matcher_type="scheme_and_host",
                                 matcher_options={"scheme": "http", "host": "example.com"})
            self.addToDatabase(ds, matcher)

    def test_show_matcher(self):
        with self.client as client:
            self.loginTestUser()

            r = client.get("/data_sources/1/matchers/1", follow_redirects=True)

            self.assertTrue(b"Match URL's scheme and hostname 'http://example.com'" in r.data)

    def test_add_matcher(self):
        with self.client as client:
            self.loginTestUser()

            form_data = {}
            form_data["matcher_type"] = "scheme_and_host"
            form_data["matcher_options-scheme"] = "ftp"
            form_data["matcher_options-host"] = "example.com"

            r = client.post("/data_sources/1/matchers/new",
                            data=form_data,
                            follow_redirects=True)

            self.assertTrue(b"Matcher saved" in r.data)
            self.assertEqual(UrlMatcher.query.filter(UrlMatcher.data_source_id == 1).count(), 2)

            added_matcher = UrlMatcher.query.filter((UrlMatcher.data_source_id == 1) & (UrlMatcher.matcher_id != 1)).first()
            self.assertEqual(added_matcher.matcher_type, "scheme_and_host")
            self.assertEqual(len(added_matcher.matcher_options.items()), 2)
            self.assertEqual(added_matcher.matcher_options["scheme"], "ftp")
            self.assertEqual(added_matcher.matcher_options["host"], "example.com")

    def test_edit_matcher(self):
        with self.client as client:
            self.loginTestUser()

            form_data = {}
            form_data["matcher_type"] = "regular_expression"
            form_data["matcher_options-pattern"] = "^ftp:\/\/example.com"

            r = client.post("/data_sources/1/matchers/1/edit",
                            data=form_data,
                            follow_redirects=True)

            self.assertTrue(b"Matcher updated" in r.data)

            edited_matcher = UrlMatcher.query.filter((UrlMatcher.data_source_id == 1) & (UrlMatcher.matcher_id == 1)).first()
            self.assertEqual(edited_matcher.matcher_type, "regular_expression")
            self.assertEqual(len(edited_matcher.matcher_options.items()), 1)
            self.assertEqual(edited_matcher.matcher_options["pattern"], "^ftp:\/\/example.com")
