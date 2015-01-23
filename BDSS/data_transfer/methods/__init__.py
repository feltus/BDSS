import os

from abc import ABCMeta, abstractmethod


## Output path (relative to the job directory) for the given data URL.
#  Subclasses should save downloaded data to the path specified by
#  this function.
#  @param url
def output_path(data_url):
    return os.path.join('output', data_url.split('/')[-1])

def get_downloaded_file_size(data_url):
    return os.stat(output_path(data_url)).st_size


class BaseTransferMethod():

    __metaclass__ = ABCMeta

    def __init__(self, reporter, **kwargs):
        self.reporter = reporter
        for option, value in kwargs.iteritems():
            setattr(self, option, value)

    @abstractmethod
    def transfer_data(self, data_urls):
        pass
