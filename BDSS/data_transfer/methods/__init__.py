import md5

from datetime import datetime
from os import path

from abc import ABCMeta, abstractmethod

class BaseTransferMethod():

    __metaclass__ = ABCMeta

    def __init__(self, app_url, job_id, **kwargs):
        self.app_url = app_url
        self.job_id = job_id
        for option, value in kwargs.iteritems():
            setattr(self, option, value)

    ## Output path (relative to the job directory) for the given data URL.
    #  Subclasses should save downloaded data to the path specified by
    #  this function.
    #  @param url
    def output_path(self, data_url):
        return path.join('output', md5.new(data_url).hexdigest() + '.data')

    def report_transfer_started(self, data_url, time_started=None):
        time = time or datetime.now()
        # TODO: Implement this
        pass

    def report_transfer_time(self, data_url, measured_time):
        # TODO: Implement this
        pass

    def report_transfer_finished(self, data_url, error=None, time_started=None):
        time = time or datetime.now()
        # TODO: Implement this
        pass

    @abstractmethod
    def transfer_data(self, data_urls):
        pass
