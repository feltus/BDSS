import json
import uuid

from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import backref, relationship, Session

from ..common import config
from .common import BaseModel, validates, ValidationMixin

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

    ## @var error_message
    #  Error message reported if job could not be started.
    error_message = Column(Text())

    ## @var reporting_token
    #  Token used by destination to report status updates for this job.
    reporting_token = Column(String(32))

    ## Generate a unique reporting token for this job.
    def generate_reporting_token(self):
        token = uuid.uuid4().hex
        session = Session.object_session(self)
        while session.query(self.__class__).filter_by(reporting_token=token).first() is not None:
            token = uuid.uuid4().hex

        self.reporting_token = token

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
            'error': self.error_message
        }
