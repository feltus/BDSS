import importlib
import yaml

from os import listdir, path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Dynamically import a class where the class name is based on its module's name.
#  Ex.import_class('package', 'module_name', 'Suffix')
#  imports and returns package.module_name.ModuleNameSuffix
#
#  @param package The package containing the class's module
#  @param module  The name of the module containing the class
#  @param suffix  Suffix to append to the class name derived from the module name.
def import_class(package, module, suffix):
    module_path = package + '.' + module
    class_name =  ''.join([s.capitalize() for s in module.split('_')]) + suffix
    module = importlib.import_module(module_path, __package__)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError()


## App configuration.
config = {}
config_dir = path.join(path.dirname(path.realpath(__file__)), 'config')
for config_file in listdir(config_dir):
    config_file_path = path.join(config_dir, config_file)
    (file_name, extension) = path.splitext(config_file)
    if path.isfile(config_file_path) and extension == '.yml':
        config[file_name] = yaml.load(open(config_file_path, 'r').read())

# Add requires_ssh_key value for data destinations.
# True if the destination's file transfer method or job execution method
# requires an SSH key.
for dest in config['data_destinations']:
    file_transfer_module = config['data_destinations'][dest]['file_transfer']['module']
    file_transfer_class = import_class('.data_destinations.file_transfer', file_transfer_module, 'FileTransferMethod')

    job_execution_module = config['data_destinations'][dest]['job_execution']['module']
    job_execution_class = import_class('.data_destinations.execution', job_execution_module, 'ExecutionMethod')

    config['data_destinations'][dest]['requires_ssh_key'] = file_transfer_class.requires_ssh_key or job_execution_class.requires_ssh_key


## Database object for app.
db_engine = create_engine(config['app']['database_url'])
DBSession = sessionmaker(bind=db_engine)
