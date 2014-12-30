import importlib
import yaml

from os import listdir, path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## App configuration.
config = {}
config_dir = path.join(path.dirname(path.realpath(__file__)), 'config')
for config_file in listdir(config_dir):
    config_file_path = path.join(config_dir, config_file)
    (file_name, extension) = path.splitext(config_file)
    if path.isfile(config_file_path) and extension == '.yml':
        config[file_name] = yaml.load(open(config_file_path, 'r').read())

## Database object for app.
db_engine = create_engine(config['app']['database_url'])
DBSession = sessionmaker(bind=db_engine)

## Dynamically import a class.
#  @param class_path
def import_class(package, module, suffix):
    module_path = package + '.' + module
    class_name =  ''.join([s.capitalize() for s in module.split('_')]) + suffix
    module = importlib.import_module(module_path, __package__)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError()
