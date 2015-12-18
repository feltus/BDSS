import datetime

import sqlalchemy as sa
from flask.ext.jsontools.formatting import get_entity_loaded_propnames
from flask.ext.login import current_user, UserMixin
from sqlalchemy.orm import backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .config import app_config
from .util import matcher_of_type, transform_of_type, JSONEncodedDict, MutableDict

# http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
db_engine = sa.create_engine(app_config["database_url"])
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


class DataSource(BaseModel, TrackEditsMixin):

    __tablename__ = "data_sources"

    id = sa.Column(sa.types.Integer(), autoincrement=True, primary_key=True, nullable=False)

    label = sa.Column(sa.types.String(100), index=True, nullable=False, unique=True)

    description = sa.Column(sa.types.Text())

    transfer_mechanism_type = sa.Column(sa.types.String(100), nullable=False)

    transfer_mechanism_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    def __repr__(self):
        return "<DataSource (id=%s, label=%s)>" % (self.id, self.label)

    def matches_url(self, url):
        for matcher in self.url_matchers:
            if matcher.matches_url(url):
                return True
        return False


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


class Transform(BaseModel, TrackEditsMixin):

    __tablename__ = "url_transforms"

    transform_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=False, nullable=False)

    from_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    from_data_source = sa.orm.relationship("DataSource",
                                           backref=backref("transforms", cascade="all, delete-orphan"),
                                           foreign_keys=[from_data_source_id])

    to_data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), nullable=False)

    to_data_source = sa.orm.relationship("DataSource",
                                         backref=backref("targeting_transforms", cascade="all, delete-orphan"),
                                         foreign_keys=[to_data_source_id])

    transform_type = sa.Column(sa.types.String(100), nullable=False)

    transform_options = sa.Column(MutableDict.as_mutable(JSONEncodedDict), default={}, nullable=False)

    description = sa.Column(sa.types.Text())

    def __repr__(self):
        return "<Transform (from_data_source=%d, transform_id=%d)>" % (self.from_data_source_id, self.transform_id)

    def transform_url(self, url):
        return transform_of_type(self.transform_type)(self.transform_options, url)


class TimingReport(BaseModel):

    __tablename__ = "timing_reports"

    report_id = sa.Column(sa.types.Integer(), primary_key=True, autoincrement=False, nullable=False)

    data_source_id = sa.Column(sa.types.Integer(), sa.ForeignKey("data_sources.id"), primary_key=True, nullable=False)

    data_source = sa.orm.relationship("DataSource",
                                      backref=backref("timing_reports", cascade="all, delete-orphan"),
                                      foreign_keys=[data_source_id])

    url = sa.Column(sa.types.Text(), nullable=False)

    file_size_bytes = sa.Column(sa.types.Integer(), nullable=False)

    transfer_duration_seconds = sa.Column(sa.types.Float(), nullable=False)

    created_at = sa.Column(sa.types.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<TimingReport (data_source=%d, url=%s, time=%f)>" % (self.data_source_id, self.url, self.transfer_duration_seconds)


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
