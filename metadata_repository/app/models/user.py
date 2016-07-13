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

import sqlalchemy as sa
from flask_login import UserMixin

from .base import BaseModel


class User(BaseModel, UserMixin):

    __tablename__ = "users"

    user_id = sa.Column(sa.types.Integer(), primary_key=True, nullable=False)

    def get_id(self):
        return str(self.user_id)

    name = sa.Column(sa.types.String(100), nullable=False)

    email = sa.Column(sa.types.String(100), nullable=False, unique=True)

    password_hash = sa.Column(sa.types.String(80), nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    last_updated_at = sa.Column(sa.types.DateTime(), nullable=False)

    is_active = sa.Column(sa.types.Boolean(), default=True, nullable=False)

    is_admin = sa.Column(sa.types.Boolean(), default=False, nullable=False)
