#!/usr/bin/python

import sys
import logging
from os.path import dirname, realpath

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, dirname(realpath(__file__)))

from BDSS import app as application
