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
from ..util import transform_of_type


transform_destination_association = sa.Table(
    "transform_destinations",
    BaseModel.metadata,
    sa.Column("transform_from_data_source_id", sa.types.Integer),
    sa.Column("transform_id", sa.types.Integer),
    sa.Column("destination_id", sa.types.Integer, sa.ForeignKey("destinations.id", ondelete="CASCADE")),
    sa.ForeignKeyConstraint(
        ("transform_from_data_source_id", "transform_id"),
        ("url_transforms.from_data_source_id", "url_transforms.transform_id")))


class Transform(BaseModel, TrackEditsMixin):

    __tablename__ = "url_transforms"

    transform_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=False, nullable=False)

    from_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    from_data_source = sa.orm.relationship("DataSource",
                                           backref=backref("transforms", cascade="all, delete-orphan",
                                                           order_by="Transform.preference_order"),
                                           foreign_keys=[from_data_source_id])

    to_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), nullable=False)

    to_data_source = sa.orm.relationship("DataSource",
                                         backref=backref("targeting_transforms", cascade="all, delete-orphan"),
                                         foreign_keys=[to_data_source_id])

    for_destinations = sa.orm.relationship("Destination",
                                           secondary=transform_destination_association)

    preference_order = sa.Column(sa.types.Integer(), nullable=False)

    transform_type = sa.Column(sa.types.String(100), nullable=False)

    transform_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    description = sa.Column(sa.types.Text())

    def __repr__(self):
        return "<Transform (from_data_source=%d, transform_id=%d)>" % (self.from_data_source_id, self.transform_id)

    def transform_url(self, url):
        return transform_of_type(self.transform_type)(self.transform_options, url)
