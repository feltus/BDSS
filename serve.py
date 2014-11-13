#!/usr/bin/python

import sys
from os.path import dirname, realpath

sys.path.insert(0, dirname(realpath(__file__)))

from BDSS import app as application

if __name__ == '__main__':
    application.run(debug=True)
