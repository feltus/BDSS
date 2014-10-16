import sys

from os import path
from unittest import TextTestRunner

sys.path.insert(0, path.join(path.dirname(path.realpath(__file__)), '..'))

from .run import RunJobTestCase

runner = TextTestRunner()

runner.run(RunJobTestCase())
