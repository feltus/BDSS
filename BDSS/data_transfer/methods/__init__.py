import json
import sys
import time
import urllib2

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
        return path.join('output', data_url.split('/')[-1])

    def report_status(self, data):
        url = self.app_url + '/api/jobs/' + str(self.job_id) + '/data/status'
        request = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
        try:
            f = urllib2.urlopen(request)
            response = f.read()
            f.close()
        except urllib2.HTTPError as e:
            print >> sys.stderr, 'Failed to report status: ' + json.dumps(data)

    def report_transfer_started(self, data_url, time_started=None):
        time_started = time_started or int(time.time())
        self.report_status({
            'status': 'started',
            'current_time': time_started,
            'url': data_url
        })

    def report_transfer_finished(self, data_url, time_finished=None, measured_time=None, error=None):
        time_finished = time_finished or int(time.time())
        data = {
            'status': 'finished',
            'measured_transfer_time': measured_time,
            'current_time': time_finished,
            'url': data_url
        }
        if error != None:
            data['error'] = error
        self.report_status(data)

    @abstractmethod
    def transfer_data(self, data_urls):
        pass
