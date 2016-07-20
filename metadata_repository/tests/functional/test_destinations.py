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

from app.models import Destination


class TestDestinations(BaseTestCase):

    def test_list_destinations(self):
        with self.client as client:
            self.loginTestUser()

            d = Destination(label="Test Destination")
            self.addToDatabase(d)

            r = client.get("/destinations", follow_redirects=True)

            self.assertTrue(b"Test Destination" in r.data)

    def test_add_destination(self):
        with self.client as client:
            self.loginTestUser()

            r = client.post("/destinations/new",
                            data=dict(label="Test Destination", description="A destination"),
                            follow_redirects=True)

            self.assertTrue(b"Destination saved" in r.data)
            self.assertEqual(Destination.query.count(), 1)

            added_destination = Destination.query.first()
            self.assertEqual(added_destination.label, "Test Destination")
            self.assertEqual(added_destination.description, "A destination")

    def test_prevent_duplicate_destination_label(self):
        with self.client as client:
            self.loginTestUser()

            d = Destination(label="Test Destination")
            self.addToDatabase(d)

            r = client.post("/destinations/new",
                            data=dict(label="Test Destination"),
                            follow_redirects=True)

            self.assertTrue(b"Label already taken" in r.data)
            self.assertEqual(Destination.query.count(), 1)

    def test_edit_destination(self):
        with self.client as client:
            self.loginTestUser()

            d = Destination(id=1, label="Test Destination")
            self.addToDatabase(d)

            r = client.post("/destinations/1/edit",
                            data=dict(label="Edited Destination",
                                      description="A destination"),
                            follow_redirects=True)

            self.assertTrue(b"Destination updated" in r.data)

            edited_destination = Destination.query.first()
            self.assertEqual(edited_destination.label, "Edited Destination")
            self.assertEqual(edited_destination.description, "A destination")

    def test_edit_destination_same_label(self):
        # Test for errors caused by the Unique validator on destination's label
        with self.client as client:
            self.loginTestUser()

            d = Destination(id=1, label="Test Destination")
            self.addToDatabase(d)

            r = client.post("/destinations/1/edit",
                            data=dict(label="Test Destination",
                                      description="Edited description"),
                            follow_redirects=True)

            self.assertTrue(b"Destination updated" in r.data)

            edited_destination = Destination.query.first()
            self.assertEqual(edited_destination.label, "Test Destination")
            self.assertEqual(edited_destination.description, "Edited description")

    def test_delete_destination(self):
        with self.client as client:
            self.loginTestUser()

            d = Destination(id=1, label="Test Destination")
            self.addToDatabase(d)

            r = client.post("/destinations/1/delete",
                            follow_redirects=True)

            self.assertTrue(b"Destination deleted" in r.data)
            self.assertEqual(Destination.query.count(), 0)
