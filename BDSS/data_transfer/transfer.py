#!/usr/bin/python

import json
import logging
import os
import string
import sys
import time
import urllib2

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

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

if len(sys.argv) < 2:
    print >> sys.stderr, 'Usage: run.py url_list_file'
    sys.exit(1)

url_list_file = sys.argv[1]

# Read data URLs from file.
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
method = method_class(config['app_url'], config['job_id'], config['reporting_token'], **config['init_args'])

start_time = time.time()
method.transfer_data(urls)
elapsed_time = time.time() - start_time

# Report job duration to BDSS server.
url = config['app_url'] + '/jobs/' + str(config['job_id'])
request_data = {
    'measured_time': elapsed_time
}
request = urllib2.Request(url, json.dumps(request_data), {'Content-Type': 'application/json', 'Authorization': 'token ' + config['reporting_token']})
try:
    f = urllib2.urlopen(request)
    response = f.read()
    f.close()
except urllib2.HTTPError as e:
    print >> sys.stderr, 'Failed to report job time: ' + json.dumps(data)
