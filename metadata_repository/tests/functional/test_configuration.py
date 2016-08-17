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

import io
import json
from flask import url_for

from .base import BaseTestCase

from app.models import DataSource, Destination, TransferTestFile, Transform, UrlMatcher


class TestImportConfiguration(BaseTestCase):

    def loadSampleData(self):
        with self.client:
            self.loginTestUser()

            origin_source = DataSource(
                id=1,
                label="Test Source",
                transfer_mechanism_type="curl")

            origin_source.transfer_test_files.append(TransferTestFile(
                file_id=1,
                url="http://example.com/file.txt"))

            origin_source.url_matchers.append(UrlMatcher(
                matcher_id=1,
                matcher_type="scheme_and_host",
                matcher_options=dict(scheme="http", host="example.com")))

            target_source_1 = DataSource(
                id=2,
                label="Target Source 1",
                transfer_mechanism_type="curl")

            target_source_1.url_matchers.append(UrlMatcher(
                matcher_id=1,
                matcher_type="scheme_and_host",
                matcher_options=dict(scheme="http", host="example.org")))

            target_source_2 = DataSource(
                id=3,
                label="Target Source 2",
                transfer_mechanism_type="curl")

            target_source_2.url_matchers.append(UrlMatcher(
                matcher_id=1,
                matcher_type="scheme_and_host",
                matcher_options=dict(scheme="http", host="example.net")))

            transform_1 = Transform(
                from_data_source=origin_source,
                to_data_source=target_source_1,
                transform_id=1,
                preference_order=1,
                transform_type="change_host",
                transform_options=dict(new_host="example.org"))

            dest = Destination(
                id=1,
                label="Test Destination")

            transform_2 = Transform(
                from_data_source=origin_source,
                to_data_source=target_source_2,
                for_destinations=[dest],
                transform_id=2,
                preference_order=2,
                transform_type="change_host",
                transform_options=dict(new_host="example.net"))

            self.addToDatabase(
                origin_source,
                target_source_1,
                target_source_2,
                dest,
                transform_1,
                transform_2)

    def setUp(self):
        super().setUp()

        self.serialized_sample_data_sources = [
            dict(
                label="Test Source",
                description=None,
                transfer_mechanism=dict(
                    type="curl",
                    options={}),
                test_files=[
                    "http://example.com/file.txt"
                ],
                transforms=[
                    dict(
                        target="Target Source 1",
                        for_destinations=[],
                        type="change_host",
                        options=dict(new_host="example.org")),
                    dict(
                        target="Target Source 2",
                        for_destinations=["Test Destination"],
                        type="change_host",
                        options=dict(new_host="example.net"))
                ],
                url_matchers=[
                    dict(
                        type="scheme_and_host",
                        options=dict(scheme="http", host="example.com"))
                ]),
            dict(
                label="Target Source 1",
                description=None,
                transfer_mechanism=dict(
                    type="curl",
                    options={}),
                test_files=[],
                transforms=[],
                url_matchers=[
                    dict(
                        type="scheme_and_host",
                        options=dict(scheme="http", host="example.org"))
                ]),
            dict(
                label="Target Source 2",
                description=None,
                transfer_mechanism=dict(
                    type="curl",
                    options={}),
                test_files=[],
                transforms=[],
                url_matchers=[
                    dict(
                        type="scheme_and_host",
                        options=dict(scheme="http", host="example.net"))
                ])
        ]

        self.serialized_sample_destinations = [
            dict(label="Test Destination",
                 description=None)
        ]

    def test_export_configuration(self):
        self.loadSampleData()

        response = self.client.get("/configuration/export")
        response = json.loads(response.get_data(as_text=True))

        data_sources = response["data_sources"]
        destinations = response["destinations"]

        self.assertEqual(data_sources, self.serialized_sample_data_sources)
        self.assertEqual(destinations, self.serialized_sample_destinations)

    def test_import_configuration(self):
        """Verify importing configuration file populates database correctly."""
        with self.client:
            self.loginTestUser()

            import_conf = json.dumps(dict(
                data_sources=self.serialized_sample_data_sources,
                destinations=self.serialized_sample_destinations
            ))

            response = self.client.post(
                "/configuration/import",
                data=dict(conf_file=(io.BytesIO(bytes(import_conf, "utf-8")), "conf.json")),
                follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(DataSource.query.count(), 3)
            self.assertEqual(Destination.query.count(), 1)

            data_source = DataSource.query.filter(DataSource.label == "Test Source").first()
            self.assertEqual(data_source.url_matchers[0].matcher_options["host"], "example.com")

            self.assertEqual(len(data_source.transforms), 2)
            self.assertEqual(data_source.transforms[0].transform_options["new_host"], "example.org")
            self.assertEqual(data_source.transforms[1].for_destinations[0].label, "Test Destination")

    def test_anonymous_import(self):
        """Importing configuration requires authenticated admin user."""
        import_conf = json.dumps(dict(
            data_sources=self.serialized_sample_data_sources,
            destinations=self.serialized_sample_destinations
        ))

        with self.client:
            response = self.client.post(
                "/configuration/import",
                data=dict(conf_file=(io.BytesIO(bytes(import_conf, "utf-8")), "conf.json")),
                follow_redirects=False)

            self.assertEqual(response.location, url_for("auth.login", _external=True))

    def test_import_without_data(self):
        """Throw error if no configuration file is uploaded."""
        with self.client:
            self.loginTestUser()

            response = self.client.post(
                "/configuration/import",
                data=dict(conf_file=None),
                follow_redirects=True)

            self.assertEqual(response.status_code, 400)
            response_data = response.get_data(as_text=True)
            self.assertIn("Import failed", response_data)
            self.assertIn("No configuration uploaded", response_data)

    def test_import_colliding_configuration(self):
        """
        Attempting to import a configuration that contains sources or destinations that conflict with
        what's already present in the database should not save anything
        """
        self.loadSampleData()
        with self.client:
            self.loginTestUser()

            import_conf = json.dumps(dict(
                data_sources=[
                    dict(
                        label="Test Source",
                        description="Source with label that already exists",
                        transfer_mechanism=dict(
                            type="curl",
                            options={}),
                        test_files=[],
                        transforms=[],
                        url_matchers=[])
                ],
                destinations=[
                    dict(label="A New Destination")
                ]
            ))

            response = self.client.post(
                "/configuration/import",
                data=dict(conf_file=(io.BytesIO(bytes(import_conf, "utf-8")), "conf.json")),
                follow_redirects=True)

            self.assertEqual(response.status_code, 400)
            response_data = response.get_data(as_text=True)
            self.assertIn("Import failed", response_data)
            self.assertIn("Unable to overwrite existing configuration", response_data)

            self.assertEqual(DataSource.query.count(), 3)
            self.assertIsNone(DataSource.query.filter(DataSource.label == "Test Source").first().description)
            self.assertEqual(Destination.query.count(), 1)
