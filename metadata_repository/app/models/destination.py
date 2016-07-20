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

from .base import BaseModel, TrackEditsMixin


class Destination(BaseModel, TrackEditsMixin):

    __tablename__ = "destinations"

    id = sa.Column(sa.types.Integer(), autoincrement=True, primary_key=True, nullable=False)

    label = sa.Column(sa.types.String(100), index=True, nullable=False, unique=True)

    description = sa.Column(sa.types.Text())
