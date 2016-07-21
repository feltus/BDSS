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

from app.models import db_session, BaseModel, DataSource, Destination, Transform


class TestUrlTransforms(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client:
            self.loginTestUser()

            ds1 = DataSource(id=1,
                             label="Test Source",
                             transfer_mechanism_type="curl")
            ds2 = DataSource(id=2,
                             label="Another Source",
                             transfer_mechanism_type="curl")
            transform = Transform(from_data_source_id=1,
                                  to_data_source_id=2,
                                  transform_id=1,
                                  preference_order=1,
                                  transform_type="change_host",
                                  transform_options={"new_host": "example.org"})
            self.addToDatabase(ds1, ds2, transform)

    def test_show_transform(self):
        with self.client as client:
            self.loginTestUser()

            r = client.get("/data_sources/1/transforms/1", follow_redirects=True)

            self.assertTrue(b"Change URL hostname to 'example.org'" in r.data)

    def test_add_transform(self):
        with self.client as client:
            self.loginTestUser()

            form_data = {}
            form_data["transform_type"] = "change_scheme"
            form_data["to_data_source_id"] = 2
            form_data["transform_options-new_scheme"] = "ftp"

            r = client.post("/data_sources/1/transforms/new",
                            data=form_data,
                            follow_redirects=True)

            self.assertTrue(b"Transform saved" in r.data)
            self.assertEqual(Transform.query.filter(Transform.from_data_source_id == 1).count(), 2)

            added_transform = Transform.query.filter((Transform.from_data_source_id == 1) & (Transform.transform_id != 1)).first()
            self.assertEqual(added_transform.from_data_source_id, 1)
            self.assertEqual(added_transform.to_data_source_id, 2)
            self.assertEqual(added_transform.preference_order, 2)
            self.assertEqual(added_transform.transform_type, "change_scheme")
            self.assertEqual(len(added_transform.transform_options.items()), 1)
            self.assertEqual(added_transform.transform_options["new_scheme"], "ftp")

    def test_edit_transform(self):
        with self.client as client:
            self.loginTestUser()

            form_data = {}
            form_data["transform_type"] = "change_host"
            form_data["to_data_source_id"] = 2
            form_data["transform_options-new_host"] = "example.net"

            r = client.post("/data_sources/1/transforms/1/edit",
                            data=form_data,
                            follow_redirects=True)

            self.assertTrue(b"Transform updated" in r.data)

            edited_transform = Transform.query.filter((Transform.from_data_source_id == 1) & (Transform.transform_id == 1)).first()
            self.assertEqual(edited_transform.from_data_source_id, 1)
            self.assertEqual(edited_transform.to_data_source_id, 2)
            self.assertEqual(edited_transform.preference_order, 1)
            self.assertEqual(edited_transform.transform_type, "change_host")
            self.assertEqual(len(edited_transform.transform_options.items()), 1)
            self.assertEqual(edited_transform.transform_options["new_host"], "example.net")


class TestTransformDestinationRelationship(BaseTestCase):
    """
    Test that the many to many relationship between transforms and destinations behaves as expected
    """

    def setUp(self):
        super().setUp()

        with self.client:
            self.loginTestUser()

            ds1 = DataSource(id=1,
                             label="Test Source",
                             transfer_mechanism_type="curl")

            ds2 = DataSource(id=2,
                             label="Another Source",
                             transfer_mechanism_type="curl")

            transform = Transform(from_data_source_id=1,
                                  to_data_source_id=2,
                                  transform_id=1,
                                  preference_order=1,
                                  transform_type="change_host",
                                  transform_options={"new_host": "example.org"})

            dest = Destination(id=1, label="Test Destination")

            transform.for_destinations.append(dest)

            self.addToDatabase(ds1, ds2, transform, dest)

    def test_delete_destination_removes_from_relation_collection(self):
        dest = Destination.query.first()
        db_session.delete(dest)
        db_session.commit()

        transform = Transform.query.first()
        self.assertEqual(len(transform.for_destinations), 0)

        self.assertEqual(db_session.query(BaseModel.metadata.tables["transform_destinations"]).count(), 0)

    def test_delete_transform_deletes_association_record(self):
        transform = Transform.query.first()
        db_session.delete(transform)
        db_session.commit()

        self.assertEqual(db_session.query(BaseModel.metadata.tables["transform_destinations"]).count(), 0)
        self.assertEqual(Destination.query.count(), 1)
