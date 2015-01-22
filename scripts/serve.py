#!/usr/bin/python

import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, project_dir)

from BDSS import app as application

config_dir = os.path.join(project_dir, 'BDSS', 'config')
config_files = []
for f in os.listdir(config_dir):
    fpath = os.path.join(config_dir, f)
    if os.path.isfile(fpath) and fpath.endswith('.yml'):
        config_files.append(fpath)

args = {
    'debug': True,
    'extra_files': config_files
}

if len(sys.argv) > 1 and sys.argv[1] == '--public':
    args['host'] = '0.0.0.0'

if __name__ == '__main__':
    application.run(**args)
