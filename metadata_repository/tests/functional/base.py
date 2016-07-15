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

import unittest

import app
from app.models import db_engine, db_session, BaseModel


class BaseTestCase(unittest.TestCase):

    def seedData(self):
        return []

    def setUp(self):
        BaseModel.metadata.create_all(bind=db_engine)
        app.app.config["TESTING"] = True

        for obj in self.seedData():
            db_session.add(obj)
        db_session.commit()

        self.client = app.app.test_client()

    def tearDown(self):
        BaseModel.metadata.drop_all(bind=db_engine)
