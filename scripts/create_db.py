import os
import sys

from distutils.util import strtobool
from sqlalchemy_utils import database_exists, drop_database

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from BDSS.common import config, db_engine
from BDSS.models import *

def prompt_for_confirmation(prompt):
    sys.stdout.write('%s [y/n]\n' % prompt)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')


database_url = config['app']['database_url']

if database_exists(database_url):
    if prompt_for_confirmation('Database already exists. Drop it?'):
        drop_database(database_url)
        BaseModel.metadata.create_all(db_engine)
    else:
        sys.stdout.write('Database not created\n')
else:
    BaseModel.metadata.create_all(db_engine)
