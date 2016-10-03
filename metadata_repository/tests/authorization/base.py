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

import os
import re

from flask import url_for

import app
from app.models import db_engine, db_session, BaseModel, User
from app.routes.configuration import load_configuration


class BaseAuthorizationTestMixin():

    def addToDatabase(self, *args):
        for obj in args:
            db_session.add(obj)
        db_session.commit()

    def loginUser(self):
        self.client.post("/login",
                         data=dict(email="user@example.com", password="password"),
                         follow_redirects=True)

    def loginAdmin(self):
        self.client.post("/login",
                         data=dict(email="admin@example.com", password="password"),
                         follow_redirects=True)

    def login(self):
        raise NotImplementedError

    def forbiddenEndpoints(self):
        raise NotImplementedError

    def okEndpoints(self):
        raise NotImplementedError

    def unauthorizedEndpoints(self):
        raise NotImplementedError

    def testEndpointAuthorization(self):
        forbidden_endpoints = self.forbiddenEndpoints()
        ok_endpoints = self.okEndpoints()
        unauthorized_endpoints = self.unauthorizedEndpoints()

        authorization_errors = {}
        for rule in app.app.url_map.iter_rules():
            for method in [m for m in rule.methods if m not in ("HEAD", "OPTIONS",)]:
                with app.app.test_request_context():
                    self.login()

                    args = {}
                    for arg in rule.arguments:
                        args[arg] = 1
                    endpoint_url = url_for(rule.endpoint, **args)

                    r = self.client.open(endpoint_url, method=method, follow_redirects=False)

                    try:
                        p = (rule.endpoint, method)
                        if p in forbidden_endpoints:
                            self.assertEqual(r.status_code, 403)
                        elif p in ok_endpoints:
                            self.assertNotIn(r.status_code, (401, 403))
                        elif p in unauthorized_endpoints:
                            # Some endpoints (those requested by the client) will return 401
                            # Web endpoints should redirect to login page
                            self.assertIn(r.status_code, (302, 401))
                            if r.status_code == 302:
                                redirect_location = r.headers.get("Location")
                                relative_location = re.sub(r"^https?://[^/]*", "", redirect_location)
                                self.assertIsNotNone(redirect_location)
                                self.assertEqual(relative_location, url_for("auth.login"))
                        else:
                            self.fail("%s to %s not covered in test" % (method, rule.endpoint))

                    except AssertionError as exc:
                        authorization_errors[(rule.endpoint, method)] = exc

        if authorization_errors:
            errored_endpoints = authorization_errors.keys()
            errored_endpoints = sorted(errored_endpoints, key=lambda e: " ".join(e))
            error_list = ["%s %s: %s" % (e[0], e[1], authorization_errors[e]) for e in errored_endpoints]
            self.fail("\n" + "\n".join(error_list))

    def setUp(self):
        BaseModel.metadata.drop_all(bind=db_engine)
        BaseModel.metadata.create_all(bind=db_engine)

        app.app.config["TESTING"] = True

        self.client = app.app.test_client()

        user = User(user_id=1, name="Test User", email="user@example.com", is_admin=False)
        user.set_password("password")
        self.addToDatabase(user)

        admin = User(user_id=2, name="Test Admin", email="admin@example.com", is_admin=True)
        admin.set_password("password")
        self.addToDatabase(admin)

        with self.client as c:
            self.loginAdmin()
            test_conf_path = os.path.join(os.path.dirname(__file__), "test_config.json")
            test_conf = open(test_conf_path).read()
            load_configuration(test_conf)
            c.get("/logout")

    def tearDown(self):
        BaseModel.metadata.drop_all(bind=db_engine)
