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
import json
import os

import sqlalchemy as sa
from flask_jsontools.formatting import get_entity_loaded_propnames
from flask_login import current_user
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.mutable import Mutable


# http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
db_engine = sa.create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))


@sa.event.listens_for(db_session, "before_flush")
def receive_before_flush(session, flush_context, instances):
    for obj in session.new:
        if hasattr(obj, "created_at"):
            obj.created_at = datetime.datetime.utcnow()
        if hasattr(obj, "created_by_user_id"):
            obj.created_by_user_id = current_user.user_id
        if hasattr(obj, "last_updated_at"):
            obj.last_updated_at = datetime.datetime.utcnow()
        if hasattr(obj, "last_updated_by_user_id"):
            obj.last_updated_by_user_id = current_user.user_id

    for obj in session.dirty:
        if hasattr(obj, "last_updated_at"):
            obj.last_updated_at = datetime.datetime.utcnow()
        if hasattr(obj, "last_updated_by_user_id"):
            obj.last_updated_by_user_id = current_user.user_id


class TrackEditsMixin(object):

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    @declared_attr
    def created_by_user_id(cls):
        return sa.Column(sa.types.Integer(), sa.ForeignKey("users.user_id"), nullable=False)

    @declared_attr
    def created_by(cls):
        return sa.orm.relationship("User", foreign_keys=lambda: [cls.created_by_user_id])

    last_updated_at = sa.Column(sa.types.DateTime(), nullable=False)

    @declared_attr
    def last_updated_by_user_id(cls):
        return sa.Column(sa.types.Integer(), sa.ForeignKey("users.user_id"), nullable=False)

    @declared_attr
    def last_updated_by(cls):
        return sa.orm.relationship("User", foreign_keys=lambda: [cls.last_updated_by_user_id])


class BaseModel(object):
    """Base class for models."""

    def _asdict(self):
        """
        Return a dictionary to be serialized to JSON.
        The simplejson JSONEncoder looks for this method when serializing.

        See https://github.com/kolypto/py-flask-jsontools/blob/master/flask_jsontools/formatting.py#L71

        Returns: dict
        """
        return {name: getattr(self, name) for name in get_entity_loaded_propnames(self)}


BaseModel = declarative_base(cls=BaseModel)
BaseModel.query = db_session.query_property()


class JSONEncodedDict(sa.types.TypeDecorator):
    """
    This type stores data in the database as JSON encoded text.
    However, the model's property is a dictionary.

    http://docs.sqlalchemy.org/en/latest/core/custom_types.html#marshal-json-strings
    """

    impl = sa.types.Text

    def process_bind_param(self, value, dialect):
        """Store dictionary as JSON."""
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """Load dictionary from JSON."""
        if value is not None:
            value = json.loads(value)
        return value


class MutableDict(Mutable, dict):
    """
    Used in conjunctino with JSONEncodedDict.
    By default, when a dictionary value is changed, the dictionary object is still the same object, so SQLAlchemy
    doesn't recognize the field as having changed and thus doesn't store the change in the database.

    This marks the field as having changed whenever a dictionary value is changed or a key is deleted.

    http://docs.sqlalchemy.org/en/latest/orm/extensions/mutable.html#establishing-mutability-on-scalar-column-values
    """

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."
        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."
        dict.__delitem__(self, key)
        self.changed()
