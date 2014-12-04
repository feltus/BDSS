import importlib
import logging
import json
import string
import sys
import traceback

from datetime import datetime
from itsdangerous import Signer
from os import path
from sqlalchemy.orm.session import Session
from time import sleep

from .common import config, db_engine, DBSession
from .models import Job, DataItem

## Dynamically import a class.
#  @param class_path
def import_class(subpackage, module, suffix):
    module_path = '.' + subpackage + '.' + module
    class_name =  ''.join([s.capitalize() for s in module.split('_')]) + suffix
    module = importlib.import_module(module_path, __package__)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError()

def start_job(job):

    job.started_at = datetime.utcnow()
    Session.object_session(job).commit()

    destination_config = config['data_destinations'][job.data_destination]

    # Group URLs
    data_urls = [d.data_url for d in job.required_data]
    default_grouping_module = 'no'
    try:
        grouping_module = destination_config['url_grouping'] or default_grouping_module
    except KeyError:
        grouping_module = default_grouping_module
    grouping_class = import_class('data_transfer.grouping', grouping_module, 'Grouping')
    grouping = grouping_class()

    url_groups = grouping.group_urls(data_urls)

    # Copy job files to destination.
    file_transfer_method_class = import_class('data_destinations.file_transfer', destination_config['file_transfer']['module'], 'FileTransferMethod')
    try:
        file_transfer_method_init_args = destination_config['file_transfer']['args'] or {}
    except KeyError:
        file_transfer_method_init_args = {}
    if destination_config['file_transfer']['module'] == 'sftp':
        keys = [k for k in job.owner.keys if k.destination == job.data_destination]
        file_transfer_method_init_args['user'] = keys[0].username
        file_transfer_method_init_args['key'] = keys[0].private
    file_transfer_method = file_transfer_method_class(**file_transfer_method_init_args)

    job_directory = path.join(job.destination_directory, 'bdss', 'job_%d' % job.job_id)

    file_transfer_method.connect()
    file_transfer_method.mkdir_p(job_directory)

    # Copy transfer method scripts.
    scripts_dir = path.join(job_directory, 'scripts')
    file_transfer_method.mkdir_p(path.join(scripts_dir, 'methods'))

    local_transfer_dir = path.join(path.dirname(path.realpath(__file__)), 'data_transfer')

    for p in ['methods/__init__.py', 'methods/' + job.data_transfer_method + '.py', 'transfer.py']:
        with open(path.join(local_transfer_dir, p), 'r') as f:
            file_transfer_method.transfer_file(path.join(scripts_dir, p), f.read())

    # Generate token for sending status updates.
    signer = Signer(config['app']['secret_key'])
    signed_id = signer.sign('{0},{1}'.format(job.owner.email, job.job_id))
    signature = signed_id.split('.')[-1]

    # Copy configuration
    transfer_config = {
        'app_url': config['app']['app_url'],
        'job_id': job.job_id,
        'owner': job.owner.email,
        'method': job.data_transfer_method,
        'init_args': job.data_transfer_method_options,
        'signature': signature
    }
    file_transfer_method.transfer_file(path.join(scripts_dir, 'transfer_config.json'), json.dumps(transfer_config))

    # Copy URL lists.
    file_transfer_method.mkdir_p(path.join(job_directory, 'urls'))
    i = 0
    for group_urls in url_groups:
        file_transfer_method.transfer_file(path.join(job_directory, 'urls', 'group_%d.txt' % i), '\n'.join(group_urls))
        i += 1

    # Create output directory.
    file_transfer_method.mkdir_p(path.join(job_directory, 'output'))

    file_transfer_method.disconnect()

    # Start job
    execution_method_class = import_class('data_destinations.execution', destination_config['job_execution']['module'], 'ExecutionMethod')
    try:
        execution_method_init_args = destination_config['job_execution']['args'] or {}
    except KeyError:
        execution_method_init_args = {}
    if destination_config['job_execution']['module'] == 'ssh':
        keys = [k for k in job.owner.keys if k.destination == job.data_destination]
        execution_method_init_args['user'] = keys[0].username
        execution_method_init_args['key'] = keys[0].private
    execution_method = execution_method_class(**execution_method_init_args)

    execution_method.connect()
    execution_method.execute_job(job_directory)
    execution_method.disconnect()

def start_job_loop():
    # Connect to database
    db_connection = db_engine.connect()
    db_session = DBSession(bind=db_connection)

    print 'Running'
    while True:
        print 'Checking for jobs'
        job = db_session.query(Job).filter_by(started_at=None).order_by('created_at ASC').first()
        if job:
            try:
                print 'Starting job %d' % job.job_id
                start_job(job)
            except Exception as e:
                print >> sys.stderr, 'Failed to start job %d: %s' % (job.job_id, str(e))
                print >> sys.stderr, traceback.format_exc()
        else:
            print 'Sleeping'
            sleep(60)

    # Disconnect from database.
    db_session.close()
    db_connection.close()
