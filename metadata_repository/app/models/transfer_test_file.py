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

from .base import BaseModel, TrackEditsMixin


class TransferTestFile(BaseModel, TrackEditsMixin):

    __tablename__ = "transfer_test_files"

    file_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=False, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    data_source = sa.orm.relationship("DataSource",
                                      backref=backref("transfer_test_files", cascade="all, delete-orphan"),
                                      foreign_keys=[data_source_id])

    url = sa.Column(sa.types.Text(), nullable=False)

    def __repr__(self):
        return "<TransferTestFile (data_source=%d, url=%s)>" % (self.data_source_id, self.url)
