import inspect
import json
import re

from datetime import datetime
from flask.ext.login import UserMixin
from sqlalchemy import Column, event, ForeignKey, UniqueConstraint
from sqlalchemy.types import BigInteger, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import backref, mapper, relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from .common import config, DBSession

BaseModel = declarative_base()

# From http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
_url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

_checksum_regex = re.compile('^[0-9a-f]+', re.IGNORECASE)


def validates(attribute_name):
    def validates_decorator(fn):
        fn.__validates_attribute__ = attribute_name
        return fn

    return validates_decorator

class ValidationError(Exception):

    def __init__(self, invalid_obj):
        if not isinstance(invalid_obj, list):
            self.invalid_objects = [invalid_obj]
        else:
            self.invalid_objects = invalid_obj

@event.listens_for(mapper, 'before_insert')
@event.listens_for(mapper, 'before_update')
def before_exec(mapper, connection, target):
    session = Session.object_session(target)

    if not hasattr(session, '_objs_to_validate') or not session._objs_to_validate:
        session._objs_to_validate = []

    session._objs_to_validate.append(target)

@event.listens_for(Session, 'before_commit')
def before_commit(session):
    if not hasattr(session, '_objs_to_validate') or not session._objs_to_validate:
        session._objs_to_validate = []

    for obj in session._objs_to_validate:
        if hasattr(obj, 'validate') and callable(getattr(obj, 'validate')):
            if not obj.validate():
                raise ValidationError(obj)

@event.listens_for(mapper, 'mapper_configured')
def mapper_configured(mapper, cls):
    if hasattr(cls, '_init_validation') and callable(getattr(cls, '_init_validation')):
        cls._init_validation()

class ValidationMixin:

    _validation_methods = None

    @classmethod
    def _init_validation(cls):
        for method_name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
            if hasattr(method, '__validates_attribute__'):
                if cls._validation_methods is None:
                    cls._validation_methods = {}
                cls._validation_methods[method.__validates_attribute__] = method_name

    def validate(self):
        self.validation_errors = {}

        if self.__class__._validation_methods is None:
            return True

        for attribute_name, method_name in self.__class__._validation_methods.iteritems():
            method = getattr(self, method_name)
            try:
                method(attribute_name, getattr(self, attribute_name))
            except ValueError as e:
                self.validation_errors[attribute_name] = [e.message]

        if self.validation_errors:
            return False

        return True


class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    ## @var id
    #  Unique ID for this user.
    id = Column(Integer(), primary_key=True, nullable=False)

    ## @var name
    #  User's full name.
    name = Column(String(100), nullable=False)

    ## @var email
    #  User's email address.
    email = Column(String(50), nullable=False, unique=True)

    ## @var password_hash
    password_hash = Column(String(80), nullable=False)

    ## @var jobs
    #  Jobs this user has submitted.
    jobs = relationship('Job', backref='owner')

    ## @var keys
    #  SSH keys owned by this user.
    keys = relationship('SSHKey', backref='owner')

class SSHKey(BaseModel):

    __tablename__ = 'ssh_keys'

    __table_args__ = (
        # Prevent duplicate keys for a user/host pair.
        UniqueConstraint('owner_id', 'destination', name='_duplicate_keys_constraint'),
    )

    ## @var id
    #  Unique ID for this key.
    id = Column(Integer(), primary_key=True, nullable=False)

    ## @var owner_id
    #  The ID of the user who owns this key.
    owner_id = Column(Integer(), ForeignKey('users.id'), nullable=False)

    ## @var destination
    #  The data destination this key is for. This corresponds to a key
    #  in config/data_destinations.yml.
    destination = Column(String(100), nullable=False)

    ## @var username
    #  The user's username on the destination host.
    username = Column(String(50), nullable=False)

    ## @var public
    #  The public key.
    public = Column(Text(), nullable=False)

    ## @var private
    #  The private key.
    private = Column(Text(), nullable=False)


class Job(BaseModel, ValidationMixin):

    __tablename__ = 'jobs'

    ## @var job_id
    #  Unique ID for this job.
    job_id = Column(Integer(), primary_key=True, nullable=False)

    ## @var owner_id
    #  The ID of the user who submitted this job.
    owner_id = Column(Integer(), ForeignKey('users.id'), nullable=False)

    ## @var name
    #  User supplied name for the job.
    name = Column(String(100), nullable=False)

    @validates('name')
    def validate_name(self, attribute_name, value):
        if not value:
            raise ValueError('A job name is required')

    ## @var required_data
    #  The data necessary for running this job.
    required_data = relationship('DataItem', backref='job')

    ## @var data_transfer_method
    #  The data transfer method selected by the user. Corresponds to an ID
    #  in config/data_transfer_methods.yml.
    data_transfer_method = Column(String(30), nullable=False)
    # TODO: Validate that this matches an available method.

    ## @var data_transfer_method_options
    #  User supplied arguments to be passed to the constructor of the
    #  data transfer method's class.
    _data_transfer_method_options = Column(Text(), nullable=False, default='{}')
    # TODO: Validate options are correct types, etc.

    @property
    def data_transfer_method_options(self):
        try:
            value = json.loads(self._data_transfer_method_options)
        except:
            value = {}
        return value

    @data_transfer_method_options.setter
    def data_transfer_method_options(self, value):
        value = value or {}
        self._data_transfer_method_options = json.dumps(value)

    ## @var data_destination
    #  The destination selected by the user. Corresponds to an ID in
    #  config/data_destinations.yml.
    data_destination = Column(String(30), nullable=False)

    @validates('data_destination')
    def validate_data_destination(self, attribute_name, value):
        if not value:
            raise ValueError('A destination is required')

        available_destinations = [id for id, dest in config['data_destinations'].iteritems()]
        if value not in available_destinations:
            raise ValueError(value + ' is not an available destination')

        # If the specified destination requires an SSH key, check that the
        # job's owner has a key for that destination.
        if config['data_destinations'][value]['requires_ssh_key']:
            if not [key for key in self.owner.keys if key.destination == value]:
                raise ValueError(config['data_destinations'][value]['label'] + ' requires an SSH key')

    ## @var destination_directory
    #  The directory on the destination machine to save downloaded data into.
    destination_directory = Column(Text(), nullable=False)

    @validates('destination_directory')
    def validate_destination_directory(self, attribute_name, value):
        if not value:
            raise ValueError('A destination directory is required')

    ## @var created_at
    #  The time this job was submitted.
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)

    ## @var started_at
    #  The time this job was sent to its destination and started.
    started_at = Column(DateTime())

    ## @var measured_time
    #  Time this job required to complete, from when it was started on the destination.
    measured_time = Column(Float())

    ## @var error_message
    #  Error message reported if job could not be started.
    error_message = Column(Text())

    ## Get status of this job based on status of its transfer script fragments.
    def status(self):
        if self.error_message:
            return 'failed'
        if len([d for d in self.required_data if d.status != 'pending']) == 0:
            return 'pending'
        elif len([d for d in self.required_data if d.status == 'pending' or d.status == 'in_progress']) != 0:
            return 'in_progress'
        elif len([d for d in self.required_data if d.status == 'failed']) == 0:
            return 'completed'
        else:
            return 'failed'

    def data_status_summary(self):
        statuses = ['pending', 'in_progress', 'completed', 'failed']
        return dict([(status, len([d for d in self.required_data if d.status == status])) for status in statuses])

    def __repr__(self):
        return '<Job (job_id=%s, name="%s")>' % (self.job_id, self.name)

    def serialize(self):
        return {
            'job_id': self.job_id,
            'name': self.name,
            'status': self.status(),
            'required_data': [item.serialize() for item in self.required_data],
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at and self.started_at.isoformat(),
            'measured_time': self.measured_time,
            'error': self.error_message
        }

class DataItem(BaseModel, ValidationMixin):

    __tablename__ = 'data_items'

    __table_args__ = (
            # Prevent duplicate data URLs in the same job.
            UniqueConstraint('job_id', 'data_url', name='_duplicate_urls_constraint'),
        )

    ## @var item_id
    #  Unique ID of data item.
    item_id = Column(Integer(), primary_key=True, nullable=False)

    ## @var job_id
    #  The ID of the job this data item is attached to.
    job_id = Column(Integer(), ForeignKey('jobs.job_id'), nullable=False)

    ## @var url
    #  The URL where the data file is located.
    data_url = Column(String(200), nullable=False)

    @validates('data_url')
    def validate_url(self, attribute_name, value):
        if not value:
            raise ValueError('A URL is required')
        if not _url_regex.match(value):
            raise ValueError(value + ' is not a valid URL')

    ## @var checksum
    #  Optional checksum to verify the data file against.
    checksum = Column(String(64))

    @validates('checksum')
    def validate_checksum(self, attribute_name, value):
        if value != None:
            if not _checksum_regex.match(value):
                raise ValueError('Checksums must contain only hex characters')

            # Validate that checksum if the correct length for the selected
            # checksum method.
            if self.checksum_method == 'md5' and len(value) != 32:
                raise ValueError('MD5 checksums must be 32 characters long')

    ## @var checksum_method
    #  The method used to generate the checksum.
    checksum_method = Column(Enum('md5', name='checksum_methods'), default='md5')

    ## @var group
    #  The transfer group of this job that this item has been assigned to.
    group = Column(Integer())

    ## @var error_message
    #  Error message reported by transfer method if transfer of this item failed.
    error_message = Column(Text())

    ## @var transfer_started_at
    #  Time that transfer of this data item was begun.
    transfer_started_at = Column(DateTime())

    ## @var transfer_finished_at
    #  Time that transfer of this data item was completed for failed.
    transfer_finished_at = Column(DateTime())

    ## @var measured_transfer_time
    #  Time required for transfer of this data item (in seconds).
    measured_transfer_time = Column(Float())

    ## @var transfer_size
    #  The size of the downloaded file (in bytes).
    transfer_size = Column(BigInteger())

    ## @var status
    #  The status of this fragment.
    status = Column(Enum('pending', 'in_progress', 'completed', 'failed', name='data_transfer_statuses'), default='pending', nullable=False)

    def __repr__(self):
        return '<DataItem (id=%s, job_id=%s, data_url=%s)>' % (self.item_id, self.job_id, self.data_url)

    def serialize(self):
        return {
            'item_id': self.item_id,
            'data_url': self.data_url,
            'status': self.status,
            'transfer_size': self.transfer_size,
            'transfer_time': self.measured_transfer_time,
            'started_at': self.transfer_started_at and self.transfer_started_at.isoformat(),
            'finished_at': self.transfer_finished_at and self.transfer_finished_at.isoformat(),
            'error': self.error_message
        }
