import datetime

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import app_config
from .util import matcher_of_type, JSONEncodedDict, MutableDict

# http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
db_engine = sa.create_engine(app_config["database_url"])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))

BaseModel = declarative_base()
BaseModel.query = db_session.query_property()

class DataSource(BaseModel):

    __tablename__ = "data_sources"

    id = sa.Column(sa.types.Integer(), primary_key=True, nullable=False)

    label = sa.Column(sa.types.String(100), nullable=False)

    url_matchers = sa.orm.relationship("UrlMatcher", backref="data_source", cascade="all, delete-orphan")

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

    matcher_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={})

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<UrlMatcher (id=%d)>" % (self.id)

    def matches_url(self, url):
        return matcher_of_type(self.matcher_type)(self.matcher_options, url)
