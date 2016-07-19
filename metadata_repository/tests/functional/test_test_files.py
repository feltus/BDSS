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

from app.models import DataSource, TransferTestFile, UrlMatcher


class TestTestFiles(BaseTestCase):

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
            test_file = TransferTestFile(data_source_id=1,
                                         file_id=1,
                                         url="http://example.com/file1.txt")
            self.addToDatabase(ds, matcher, test_file)

    def test_show_test_file(self):
        with self.client as client:
            self.loginTestUser()

            r = client.get("/data_sources/1/test_files/1", follow_redirects=True)

            self.assertTrue(b"http://example.com/file1.txt" in r.data)

    def test_add_test_file(self):
        with self.client as client:
            self.loginTestUser()

            r = client.post("/data_sources/1/test_files/new",
                            data=dict(url="http://example.com/file2.txt"),
                            follow_redirects=True)

            self.assertTrue(b"Test file saved" in r.data)
            self.assertEqual(TransferTestFile.query.filter(TransferTestFile.data_source_id == 1).count(), 2)

            added_file = TransferTestFile.query.filter((TransferTestFile.data_source_id == 1) & (TransferTestFile.file_id != 1)).first()
            self.assertEqual(added_file.url, "http://example.com/file2.txt")

    def test_add_non_matching_test_file(self):
        with self.client as client:
            self.loginTestUser()

            r = client.post("/data_sources/1/test_files/new",
                            data=dict(url="http://example.org/file.txt"),
                            follow_redirects=True)

            self.assertTrue(b"Test file URL does not match data source" in r.data)
            self.assertEqual(TransferTestFile.query.filter(TransferTestFile.data_source_id == 1).count(), 1)

    def test_edit_test_file(self):
        with self.client as client:
            self.loginTestUser()

            r = client.post("/data_sources/1/test_files/1/edit",
                            data=dict(url="http://example.com/file3.txt"),
                            follow_redirects=True)

            self.assertTrue(b"Test file updated" in r.data)
            edited_file = TransferTestFile.query.filter((TransferTestFile.data_source_id == 1) & (TransferTestFile.file_id == 1)).first()
            self.assertEqual(edited_file.url, "http://example.com/file3.txt")
