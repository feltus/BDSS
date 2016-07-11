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

import sqlalchemy as sa
from sqlalchemy.orm import backref

from .base import BaseModel, JSONEncodedDict, MutableDict, TrackEditsMixin
from ..util import matcher_of_type


class UrlMatcher(BaseModel, TrackEditsMixin):

    __tablename__ = "url_matchers"

    matcher_id = sa.Column(sa.types.Integer(), autoincrement=False, primary_key=True, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    data_source = sa.orm.relationship("DataSource",
                                      backref=backref("url_matchers", cascade="all, delete-orphan"),
                                      foreign_keys=[data_source_id])

    matcher_type = sa.Column(sa.types.String(100), nullable=False)

    matcher_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    def __repr__(self):
        return "<UrlMatcher (id=%d)>" % (self.id)

    def matches_url(self, url):
        return matcher_of_type(self.matcher_type)(self.matcher_options, url)
