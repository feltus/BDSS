import os
import urllib2

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

    def connect(self):
        pass

    def get_remote_file_size(self, data_url):
        # For public HTTP/FTP URLs, attempt a HEAD request.
        if data_url.lower().startswith('http://') or data_url.lower().startswith('ftp://'):
            request = urllib2.Request(data_url)
            request.get_method = lambda : 'HEAD'

            response = urllib2.urlopen(request)
            head = str(response.info())

            for line in head.split('\n'):
                if line.startswith('Content-length'):
                    return int(line.split(': ')[1])

            return None

        else:
            return None

    @abstractmethod
    def transfer_data(self, data_urls):
        pass

    def disconnect(self):
        pass
