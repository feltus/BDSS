#!/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from BDSS import app as application

args = {
    'debug': True
}

if len(sys.argv) > 1 and sys.argv[1] == '--public':
    args['host'] = '0.0.0.0'

if __name__ == '__main__':
    application.run(**args)
