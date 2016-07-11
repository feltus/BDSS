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

import statistics

import sqlalchemy as sa

from .base import BaseModel, JSONEncodedDict, MutableDict, TrackEditsMixin


class DataSource(BaseModel, TrackEditsMixin):

    __tablename__ = "data_sources"

    id = sa.Column(sa.types.Integer(), autoincrement=True, primary_key=True, nullable=False)

    label = sa.Column(sa.types.String(100), index=True, nullable=False, unique=True)

    description = sa.Column(sa.types.Text())

    transfer_mechanism_type = sa.Column(sa.types.String(100), nullable=False)

    transfer_mechanism_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    @property
    def num_successful_transfers(self):
        return len([r for r in self.transfer_reports if r.is_success])

    @property
    def mean_successful_transfer_rate(self):
        return statistics.mean([r.transfer_rate for r in self.transfer_reports if r.is_success])

    @property
    def stdev_successful_transfer_rates(self):
        return statistics.stdev([r.transfer_rate for r in self.transfer_reports if r.is_success])

    def __repr__(self):
        return "<DataSource (id=%s, label=%s)>" % (self.id, self.label)

    def matches_url(self, url):
        for matcher in self.url_matchers:
            if matcher.matches_url(url):
                return True
        return False
