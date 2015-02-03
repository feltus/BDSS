import json
import re

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import BigInteger, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import backref, relationship

from .common import BaseModel, validates, ValidationMixin

# From http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
_url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

_checksum_regex = re.compile('^[0-9a-f]+', re.IGNORECASE)

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
