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

from app.models import DataSource, Destination, Transform, UrlMatcher


class TestGetTransfers(BaseTestCase):

    def setUp(self):
        super().setUp()

        with self.client:
            self.loginTestUser()

            origin_source = DataSource(
                id=1,
                label="Test Source",
                transfer_mechanism_type="curl")

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
                transform_2
            )

    def test_get_transfers_unknown_destination(self):
        with self.client as client:
            r = client.post("/transfers",
                            data={
                                "url": "http://example.com/file.txt",
                                "available_mechanisms": ["curl"]
                            },
                            headers=dict(Accept="application/json"),
                            follow_redirects=True)

            r = json.loads(r.get_data(as_text=True))

            target_sources = [t["data_source_id"] for t in r["transfers"]]
            target_urls = [t["url"] for t in r["transfers"]]

            self.assertEqual(target_sources, [2, 1])
            self.assertEqual(target_urls, [
                "http://example.org/file.txt",
                # "http://example.net/file.txt", The transform for this only applies to one destination
                "http://example.com/file.txt"
            ])

    def test_get_transfers_known_destination(self):
        with self.client as client:
            r = client.post("/transfers",
                            data={
                                "url": "http://example.com/file.txt",
                                "available_mechanisms": ["curl"],
                                "destination": "Test Destination"
                            },
                            headers=dict(Accept="application/json"),
                            follow_redirects=True)

            r = json.loads(r.get_data(as_text=True))

            target_sources = [t["data_source_id"] for t in r["transfers"]]
            target_urls = [t["url"] for t in r["transfers"]]

            self.assertEqual(target_sources, [2, 3, 1])
            self.assertEqual(target_urls, [
                "http://example.org/file.txt",
                "http://example.net/file.txt",
                "http://example.com/file.txt"
            ])
