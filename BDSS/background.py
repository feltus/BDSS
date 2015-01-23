import logging
import json
import string
import sys
import traceback

from datetime import datetime
from os import path
from sqlalchemy.orm.session import Session
from time import sleep

from .common import config, db_engine, DBSession, import_class
from .data_destinations.execution import JobExecutionError
from .data_destinations.file_transfer import FileTransferError
from .models import Job, DataItem

def start_job(job):

    print '-------------'
    print ''
    print 'Starting job %d' % job.job_id

    job.started_at = datetime.utcnow()
    Session.object_session(job).commit()

    destination_config = config['data_destinations'][job.data_destination]
    destination_host = None
    try:
        destination_host = destination_config['host']
    except KeyError:
        pass

    # Group URLs
    data_urls = [d.data_url for d in job.required_data]
    default_grouping_module = 'no'
    try:
        grouping_module = destination_config['url_grouping'] or default_grouping_module
    except KeyError:
        grouping_module = default_grouping_module
    grouping_class = import_class('.data_transfer.grouping', grouping_module, 'Grouping')
    grouping = grouping_class()

    url_groups = grouping.group_urls(data_urls)

    # Copy job files to destination.
    file_transfer_method_class = import_class('.data_destinations.file_transfer', destination_config['file_transfer']['module'], 'FileTransferMethod')
    try:
        file_transfer_method_init_args = destination_config['file_transfer']['args'] or {}
    except KeyError:
        file_transfer_method_init_args = {}

    file_transfer_method = file_transfer_method_class(destination_host, **file_transfer_method_init_args)
    if file_transfer_method_class.requires_ssh_key:
        keys = [k for k in job.owner.keys if k.destination == job.data_destination]
        if keys:
            file_transfer_method.key = keys[0]
        else:
            job.error_message = 'Failed to transfer job files (No SSH key for destination)'
            print >> sys.stderr, job.error_message
            job.measured_time = 0
            Session.object_session(job).commit()
            return

    job_directory = path.join(job.destination_directory, 'bdss', 'job_%d' % job.job_id)

    try:
        file_transfer_method.connect()
        file_transfer_method.mkdir_p(job_directory)

        # Copy transfer method scripts.
        scripts_dir = path.join(job_directory, 'scripts')
        file_transfer_method.mkdir_p(path.join(scripts_dir, 'methods'))

        local_transfer_dir = path.join(path.dirname(path.realpath(__file__)), 'data_transfer')

        for p in ['methods/__init__.py', 'methods/' + job.data_transfer_method + '.py', 'transfer.py', 'reporting.py']:
            with open(path.join(local_transfer_dir, p), 'r') as f:
                file_transfer_method.transfer_file(path.join(scripts_dir, p), f.read())

        # Copy configuration
        transfer_config = {
            'app_url': config['app']['app_url'],
            'job_id': job.job_id,
            'method': job.data_transfer_method,
            'init_args': job.data_transfer_method_options,
            'reporting_token': job.reporting_token
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

    except FileTransferError as e:
        job.error_message = 'Failed to transfer job files (%s)' % str(e)
        print >> sys.stderr, job.error_message
        job.measured_time = 0
        Session.object_session(job).commit()
        return

    except Exception as e:
        job.error_message = 'Failed to transfer job files (Unknown error)'
        print >> sys.stderr, job.error_message
        print >> sys.stderr, traceback.format_exc()
        job.measured_time = 0
        Session.object_session(job).commit()
        return

    # Start job
    execution_method_class = import_class('.data_destinations.execution', destination_config['job_execution']['module'], 'ExecutionMethod')
    try:
        execution_method_init_args = destination_config['job_execution']['args'] or {}
    except KeyError:
        execution_method_init_args = {}

    execution_method = execution_method_class(destination_host, **execution_method_init_args)
    if execution_method_class.requires_ssh_key:
        keys = [k for k in job.owner.keys if k.destination == job.data_destination]
        if keys:
            execution_method.key = keys[0]
        else:
            job.error_message = 'Failed to execute job script (No SSH key for destination)'
            print >> sys.stderr, job.error_message
            job.measured_time = 0
            Session.object_session(job).commit()
            return

    try:
        execution_method.connect()
        if not execution_method.test_connection(config['app']['app_url']):
            raise JobExecutionError('Destination is unable to reach BDSS server')
        execution_method.execute_job(job_directory)
        execution_method.disconnect()

    except JobExecutionError as e:
        job.error_message = 'Failed to execute job script (%s)' % str(e)
        print >> sys.stderr, job.error_message
        job.measured_time = 0
        Session.object_session(job).commit()
        return

    except Exception:
        job.error_message = 'Failed to execute job script (Unknown error)'
        print >> sys.stderr, job.error_message
        print >> sys.stderr, traceback.format_exc()
        job.measured_time = 0
        Session.object_session(job).commit()
        return

    print 'Success'


def start_job_loop():
    # Connect to database
    db_connection = db_engine.connect()
    db_session = DBSession(bind=db_connection)

    print 'Running'
    while True:
        job = db_session.query(Job).filter_by(started_at=None).order_by('created_at ASC').first()
        if job:
            try:
                start_job(job)
            except Exception as e:
                job.error_message = 'Failed to start job (Unknown error)'
                print >> sys.stderr, job.error_message
                print >> sys.stderr, traceback.format_exc()
                Session.object_session(job).commit()
        else:
            sleep(60)

    # Disconnect from database.
    db_session.close()
    db_connection.close()
