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


class TestLogin(BaseTestCase):

    def test_login_logout(self):
        r = self.client.post("/login",
                             data=dict(email="user@example.com",
                                       password="password"),
                             follow_redirects=True)

        self.assertTrue(b"Test User" in r.data)

        r = self.client.get("/logout", follow_redirects=True)

        # Try to load an authenticated route
        r = self.client.get("/users", follow_redirects=True)
        self.assertTrue(b"Login" in r.data)

    def test_login_with_wrong_password_fails(self):
        r = self.client.post("/login",
                             data=dict(email="user@example.com",
                                       password="wrong"),
                             follow_redirects=True)

        self.assertTrue(b"Invalid credentials" in r.data)
