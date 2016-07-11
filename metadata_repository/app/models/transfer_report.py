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

import datetime
import math

import sqlalchemy as sa
from sqlalchemy.orm import backref

from .base import BaseModel


class TransferReport(BaseModel):

    __tablename__ = "transfer_reports"

    report_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=False, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    data_source = sa.orm.relationship("DataSource",
                                      backref=backref("transfer_reports", cascade="all, delete-orphan"),
                                      foreign_keys=[data_source_id])

    url = sa.Column(sa.types.Text(), nullable=False)

    file_size_bytes = sa.Column(sa.types.Integer(), nullable=False)

    transfer_duration_seconds = sa.Column(sa.types.Float(), nullable=False)

    @property
    def transfer_rate(self):
        return self.file_size_bytes / self.transfer_duration_seconds

    @property
    def is_transfer_rate_outlier(self):
        if self.data_source.num_successful_transfers < 3:
            return False
        else:
            avg = self.data_source.mean_successful_transfer_rate
            stdev = self.data_source.stdev_successful_transfer_rates
            return math.fabs(self.transfer_rate - avg) > 3 * stdev

    file_checksum = sa.Column(sa.types.String(32), nullable=False)

    mechanism_output = sa.Column(sa.types.Text())

    is_success = sa.Column(sa.types.Boolean(), default=True, nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<TransferReport (data_source=%d, url=%s, time=%f)>" % (self.data_source_id, self.url, self.transfer_duration_seconds)
