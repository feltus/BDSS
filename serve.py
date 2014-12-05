#!/usr/bin/python

import sys
from os.path import dirname, realpath

sys.path.insert(0, dirname(realpath(__file__)))

from BDSS import app as application

args = {
    'debug': True
}

if len(sys.argv) > 1 and sys.argv[1] == '--public':
    args['host'] = '0.0.0.0'

if __name__ == '__main__':
    application.run(**args)
