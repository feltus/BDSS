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

from app.models import DataSource


class TestDataSources(BaseTestCase):

    def test_list_sources(self):
        with self.client as client:
            self.loginTestUser()

            ds = DataSource(label="Test Source", transfer_mechanism_type="curl")
            self.addToDatabase(ds)

            r = client.get("/data_sources", follow_redirects=True)

            self.assertTrue(b"Test Source" in r.data)

    def test_add_source(self):
        with self.client as client:
            self.loginTestUser()

            ds = DataSource(label="Test Source", transfer_mechanism_type="curl")
            self.addToDatabase(ds)

            r = client.post("/data_sources/new",
                            data=dict(label="Another Source",
                                      transfer_mechanism_type="curl"),
                            follow_redirects=True)

            self.assertTrue(b"Data source saved" in r.data)
            self.assertEqual(DataSource.query.count(), 2)

    def test_prevent_duplicate_source_label(self):
        with self.client as client:
            self.loginTestUser()

            ds = DataSource(label="Test Source", transfer_mechanism_type="curl")
            self.addToDatabase(ds)

            r = client.post("/data_sources/new",
                            data=dict(label="Test Source",
                                      transfer_mechanism_type="curl"),
                            follow_redirects=True)

            self.assertTrue(b"Label already taken" in r.data)
            self.assertEqual(DataSource.query.count(), 1)

    def test_edit_source(self):
        with self.client as client:
            self.loginTestUser()

            ds = DataSource(id=1, label="Test Source", transfer_mechanism_type="curl")
            self.addToDatabase(ds)

            r = client.post("/data_sources/1/edit",
                            data=dict(label="Renamed Source",
                                      transfer_mechanism_type="curl"),
                            follow_redirects=True)

            self.assertTrue(b"Data source updated" in r.data)
            self.assertEqual(DataSource.query.first().label, "Renamed Source")
