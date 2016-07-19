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

from app.models import User


class TestRegistration(BaseTestCase):

    def test_registration(self):
        r = self.client.post("/register",
                             data=dict(name="New User",
                                       email="new@example.com",
                                       password="password",
                                       password_confirmation="password"),
                             follow_redirects=True)

        self.assertTrue(b"Registration successful" in r.data)
        self.assertEqual(User.query.count(), 2)

    def test_registration_password_confirmation(self):
        r = self.client.post("/register",
                             data=dict(name="New User",
                                       email="new@example.com",
                                       password="password",
                                       password_confirmation="different"),
                             follow_redirects=True)

        self.assertTrue(b"Passwords do not match" in r.data)
        self.assertEqual(User.query.count(), 1)

    def test_prevent_duplicate_registrations(self):
        r = self.client.post("/register",
                             data=dict(name="Test User",
                                       email="user@example.com",
                                       password="password",
                                       password_confirmation="password"),
                             follow_redirects=True)

        self.assertTrue(b"Email already taken" in r.data)
        self.assertEqual(User.query.count(), 1)
