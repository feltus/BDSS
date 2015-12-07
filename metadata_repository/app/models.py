import datetime

import sqlalchemy as sa
from flask.ext.jsontools.formatting import get_entity_loaded_propnames
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import app_config
from .util import matcher_of_type, transform_of_type, JSONEncodedDict, MutableDict

# http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
db_engine = sa.create_engine(app_config["database_url"])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))


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


class DataSource(BaseModel):

    __tablename__ = "data_sources"

    id = sa.Column(sa.types.Integer(), primary_key=True, nullable=False)

    label = sa.Column(sa.types.String(100), nullable=False)

    url_matchers = sa.orm.relationship("UrlMatcher", backref="data_source", cascade="all, delete-orphan")

    transfer_mechanism_type = sa.Column(sa.types.String(100), nullable=False)

    transfer_mechanism_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<DataSource (id=%s, label=%s)>" % (self.id, self.label)

    def matches_url(self, url):
        for matcher in self.url_matchers:
            if matcher.matches_url(url):
                return True
        return False


class UrlMatcher(BaseModel):

    __tablename__ = "url_matchers"

    id = sa.Column(sa.types.Integer(), primary_key=True, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), nullable=False)

    matcher_type = sa.Column(sa.types.String(100), nullable=False)

    matcher_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<UrlMatcher (id=%d)>" % (self.id)

    def matches_url(self, url):
        return matcher_of_type(self.matcher_type)(self.matcher_options, url)


class Transform(BaseModel):

    __tablename__ = "url_transforms"

    transform_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=True, nullable=False)

    from_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    from_data_source = sa.orm.relationship("DataSource", backref="transforms", foreign_keys=[from_data_source_id])

    to_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), nullable=False)

    to_data_source = sa.orm.relationship("DataSource", backref="targeting_transforms", foreign_keys=[to_data_source_id])

    transform_type = sa.Column(sa.types.String(100), nullable=False)

    transform_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    description = sa.Column(sa.types.Text())

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Transform (from_data_source=%d, transform_id=%d)>" % (self.from_data_source_id, self.transform_id)

    def transform_url(self, url):
        return transform_of_type(self.transform_type)(self.transform_options, url)


class TimingReport(BaseModel):

    __tablename__ = "timing_reports"

    report_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=True, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    data_source = sa.orm.relationship("DataSource", backref="timing_reports", foreign_keys=[data_source_id])

    url = sa.Column(sa.types.Text(), nullable=False)

    file_size_bytes = sa.Column(sa.types.Integer(), nullable=False)

    transfer_duration_seconds = sa.Column(sa.types.Float(), nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<TimingReport (data_source=%d, url=%s, time=%f)>" % (self.data_source_id, self.url, self.transfer_duration_seconds)
