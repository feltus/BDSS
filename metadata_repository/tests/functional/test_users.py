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


class TestUsers(BaseTestCase):

    def test_list_users(self):
        with self.client as client:
            self.loginTestUser()

            u = User(email="user2@example.com", name="Another User", is_admin=False)
            u.set_password("password")
            self.addToDatabase(u)

            r = client.get("/users", follow_redirects=True)

            self.assertTrue(b"Test User" in r.data)
            self.assertTrue(b"Another User" in r.data)

    def test_show_user(self):
        with self.client as client:
            self.loginTestUser()

            u = User(user_id=2, email="user2@example.com", name="Another User", is_admin=False)
            u.set_password("password")
            self.addToDatabase(u)

            r = client.get("/users/2", follow_redirects=True)

            u = User.query.filter(User.user_id == 2).first()
            self.assertIn(u.name.encode("utf-8"), r.data)
            self.assertIn(u.email.encode("utf-8"), r.data)

    def test_toggle_admin_permissions(self):
        with self.client as client:
            self.loginTestUser()

            u = User(user_id=2, email="user2@example.com", name="Another User", is_admin=False)
            u.set_password("password")
            self.addToDatabase(u)

            r = client.post("/users/2/edit_permissions", follow_redirects=True)

            u = User.query.filter(User.user_id == 2).first()
            self.assertTrue(b"Permissions updated" in r.data)
            self.assertTrue(u.is_admin)
