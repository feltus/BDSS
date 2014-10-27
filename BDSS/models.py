import json
import re

from datetime import datetime
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import BigInteger, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.ext.declarative import declarative_base

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

class Job(BaseModel):

    __tablename__ = 'jobs'

    ## @var job_id
    #  Unique ID for this job.
    job_id = Column(Integer(), primary_key=True, nullable=False)

    ## @var name
    #  User supplied name for the job.
    name = Column(String(100), nullable=False)

    ## @var email
    #  Email address to send notifications to.
    email = Column(String(50), nullable=False)
    # TODO: Validate the format.

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
    # TODO: Validate that this matches an available destination.

    ## @var created_at
    #  The time this job was submitted.
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)

    ## @var started_at
    #  The time this job was sent to its destination and started.
    started_at = Column(DateTime())

    ## @var measured_time
    #  Time this job required to complete, from when it was started on the destination.
    measured_time = Column(Float())

    ## Get status of this job based on status of its transfer script fragments.
    def status(self):
        if len([d for d in self.required_data if d.status != 'pending']) == 0:
            return 'pending'
        elif len([d for d in self.required_data if d.status == 'pending' or d.status == 'in_progress']) != 0:
            return 'in_progress'
        elif len([d for d in self.required_data if d.status == 'failed']) == 0:
            return 'completed'
        else:
            return 'failed'

    def __repr__(self):
        return '<Job (job_id=%d, name="%s")>' % (self.job_id, self.name)

    def serialize(self):
        return {
            'job_id': self.job_id,
            'name': self.name,
            'email': self.email,
            'status': self.status(),
            'required_data': [item.serialize() for item in self.required_data],
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at and self.started_at.isoformat(),
            'measured_time': self.measured_time
        }

class DataItem(BaseModel):

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
    def validate_url(self, key, url):
        if not _url_regex.match(url):
            raise ValueError(url + ' is not a valid URL')
        return url

    ## @var checksum
    #  Optional checksum to verify the data file against.
    checksum = Column(String(64))

    @validates('checksum')
    def validate_checksum(self, key, checksum):
        if checksum != None:
            if not _checksum_regex.match(checksum):
                raise ValueError('Checksums must contain only hex characters.')

            # Validate that checksum if the correct length for the selected
            # checksum method.
            elif self.checksum_method == 'md5' and len(checksum) != 32:
                raise ValueError('MD5 checksums must be 32 characters long.')
        return checksum

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
        return '<DataItem (id=%d, job_id=%d, url=%s)>' % (self.item_id, self.job_id, self.url)

    def serialize(self):
        return {
            'item_id': self.item_id,
            'data_url': self.data_url,
            'status': self.status,
            'transfer_size': self.transfer_size
        }
