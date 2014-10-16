#!/usr/bin/python

import json
import string
import sys
import logging

from os import path

def import_class(class_path):
    (module_path, class_name) = string.rsplit(class_path, '.', 1)
    module = __import__(module_path, fromlist=[class_name])
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError()

logging.basicConfig(stream=sys.stderr)

containing_directory = path.dirname(path.realpath(__file__))
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
with open(path.join(containing_directory, 'transfer_config.json')) as f:
    config = json.load(f)

# Import transfer method class.
method_name = config['method']
class_path = 'methods.' + \
    method_name + '.' + \
    ''.join([s.capitalize() for s in method_name.split('_')]) + 'TransferMethod'
method_class = import_class(class_path)
method = method_class(config['app_url'], config['job_id'], **config['init_args'])

method.transfer_data(urls)
