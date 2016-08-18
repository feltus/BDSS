#!/usr/bin/env python3

import logging
import os
import sys

from dotenv import load_dotenv


logging.basicConfig(stream=sys.stderr)

containing_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, containing_dir)

load_dotenv(os.path.join(containing_dir, ".env"))


from app import app as application
