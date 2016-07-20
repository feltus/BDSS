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

from .base import BaseTestCase

from app.models import DataSource, Destination, TransferReport, UrlMatcher


class TestTransferReports(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client:
            self.loginTestUser()

            ds = DataSource(id=1, label="Test Source", transfer_mechanism_type="curl")

            matcher = UrlMatcher(data_source_id=1,
                                 matcher_id=1,
                                 matcher_type="scheme_and_host",
                                 matcher_options={"scheme": "http", "host": "example.com"})

            dest = Destination(id=1, label="Test destination")

            self.addToDatabase(ds, matcher, dest)

    def test_add_transfer_report_without_destination(self):
        with self.client as client:

            report = dict(
                is_success=True,
                url="http://example.com/file.txt",
                destination="",
                file_size_bytes=1000,
                transfer_duration_seconds=10,
                file_checksum="a" * 32
            )

            r = client.post("/transfer_reports",
                            data=report,
                            follow_redirects=True)

            r = json.loads(r.get_data(as_text=True))

            self.assertTrue(r["success"])
            self.assertEqual(TransferReport.query.count(), 1)

            report = TransferReport.query.first()
            self.assertEqual(report.data_source_id, 1)
            self.assertEqual(report.destination_id, None)
            self.assertEqual(report.url, "http://example.com/file.txt")
            self.assertEqual(report.file_size_bytes, 1000)
            self.assertEqual(report.transfer_duration_seconds, 10)
            self.assertEqual(report.file_checksum, "a" * 32)

    def test_add_transfer_report_with_destination(self):
        with self.client as client:

            report = dict(
                is_success=True,
                url="http://example.com/file.txt",
                destination="Test destination",
                file_size_bytes=1000,
                transfer_duration_seconds=10,
                file_checksum="a" * 32
            )

            r = client.post("/transfer_reports",
                            data=report,
                            follow_redirects=True)

            r = json.loads(r.get_data(as_text=True))

            self.assertTrue(r["success"])
            self.assertEqual(TransferReport.query.count(), 1)

            report = TransferReport.query.first()
            self.assertEqual(report.data_source_id, 1)
            self.assertEqual(report.destination_id, 1)
            self.assertEqual(report.url, "http://example.com/file.txt")
            self.assertEqual(report.file_size_bytes, 1000)
            self.assertEqual(report.transfer_duration_seconds, 10)
            self.assertEqual(report.file_checksum, "a" * 32)
