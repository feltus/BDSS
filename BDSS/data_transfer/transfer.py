#!/usr/bin/python

import json
import logging
import multiprocessing
import os
import Queue
import string
import sys
import time
import traceback
import urllib2

from methods import output_path
from reporting import JobStatusReporter

## Fake file-like stream object that redirects writes to a logger instance.
class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass # Necessary to work with multiprocessing

def import_class(class_path):
    (module_path, class_name) = string.rsplit(class_path, '.', 1)
    module = __import__(module_path, fromlist=[class_name])
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError()

# Redirect stdout,stderr to log file
containing_directory = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(
    filename=os.path.join(containing_directory, 'transfer.log'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filemode='w'
)

stdout_logger = logging.getLogger('STDOUT')
stderr_logger = logging.getLogger('STDERR')

sys.stdout = StreamToLogger(stdout_logger, logging.INFO)
sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

sys.path.insert(0, containing_directory)

# Read data URLs from file.
url_list_file = sys.argv[1]
urls = None
with open(url_list_file, 'r') as f:
    urls = f.read().rstrip().split('\n')

# Read config from file.
config = None
with open(os.path.join(containing_directory, 'transfer_config.json')) as f:
    config = json.load(f)

# Import transfer method class.
method_name = config['method']
class_path = 'methods.' + \
    method_name + '.' + \
    ''.join([s.capitalize() for s in method_name.split('_')]) + 'TransferMethod'
method_class = import_class(class_path)
method = method_class(**config['init_args'])

method.connect()

expected_file_sizes = { url: method.get_remote_file_size(url) for url in urls }

def do_transfer(transfer_method, data_urls, report_queue):

    reporter = JobStatusReporter(report_queue)

    start_time = time.time()
    method.transfer_data(reporter, urls)
    elapsed_time = time.time() - start_time


def verify_download(data_url):
    file_size = os.stat(output_path(data_url)).st_size
    if data_url in expected_file_sizes.keys() and file_size != expected_file_sizes[data_url]:
        raise ValueError('Download does not match expected file size')

    # TODO: Verify against checksum if one is available


def send_report(report):
    url = config['app_url'] + '/jobs/' + str(config['job_id']) + '/status'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + config['reporting_token']
    }
    request = urllib2.Request(url, json.dumps(status_report), headers)
    try:
        f = urllib2.urlopen(request)
        response = f.read()
        f.close()
    except urllib2.HTTPError as e:
        print >> sys.stderr, 'Failed to report status: ' + json.dumps(data)
        traceback.print_exc()


report_queue = multiprocessing.Queue()

transfer_process = multiprocessing.Process(target=do_transfer, args=(method, urls, report_queue,))
transfer_process.start()

while True:
    try:
        status_report = report_queue.get(block=True, timeout=3.0)

        if status_report['status'] == 'finished':
            try:
                verify_download(status_report['url'])
            except ValueError as e:
                status_report['error'] = e.message

        send_report(status_report)

    except Queue.Empty:
        # If the transfer process is dead, there will be no more reports.
        if not transfer_process.is_alive():
            break

method.disconnect()
