from datetime import datetime
from flask import abort, Blueprint, g, render_template, request
from flask.ext.login import current_user, login_required

from ..common import config
from ..models import Job, DataItem
from ..routes.util import filter_params, json_response

job_routes = Blueprint('jobs', __name__)

@job_routes.route('')
@login_required
def jobs_index():
    jobs = g.db_session.query(Job).filter_by(owner=current_user).all()
    return render_template('jobs/index.html.jinja', jobs=jobs)

@job_routes.route('/<job_id>', methods=['GET'])
@login_required
def show_job_page(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    if job == None:
        abort(404)
    elif job.owner != current_user:
        abort(403)
    else:
        return render_template('jobs/show.html.jinja', job=job)

@job_routes.route('/submit', methods=['GET'])
@login_required
def submit_page():
    transfer_methods = [{'id': id, 'label': method.get('label', id), 'description': method.get('description', None), 'options': method.get('options', None)} for (id, method) in config['data_transfer_methods'].iteritems()]

    destinations = [{'id': id, 'label': dest.get('label', id), 'description': dest.get('description', None)} for (id, dest) in config['data_destinations'].iteritems()]

    return render_template('jobs/submit.html.jinja', transfer_methods=transfer_methods, destinations=destinations)

@job_routes.route('', methods=['POST'])
@login_required
def create_job():
    params = request.get_json()

    job_params = filter_params(params['job'], ['name', 'data_transfer_method', 'data_transfer_method_options', 'data_destination', 'destination_directory'])

    data_params = [filter_params(p, ['data_url', 'checksum', 'checksum_method']) for p in params['job']['required_data']]

    job = Job(**job_params)
    job.owner = current_user
    for p in data_params:
        job.required_data.append(DataItem(**p))

    try:
        g.db_session.add(job)
        g.db_session.commit()
        return json_response({'job': job.serialize()}, status=201)
    except ValueError as e:
        g.db_session.rollback()
        return json_response({'errors': [str(e)]}, status=400)

@job_routes.route('/<job_id>', methods=['POST'])
@login_required
def update_job(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    params = request.get_json()

    if job == None:
        abort(404)
    elif job.owner != current_user:
        abort(403)
    else:
        job.measured_time = params['measured_time']
        g.db_session.commit()
        return json_response({'job': job.serialize()})

@job_routes.route('/<job_id>/data/status', methods=['POST'])
@login_required
def update_transfer_status(job_id):
    params = request.get_json()

    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    if job == None:
        abort(404)
    elif job.owner != current_user:
        abort(403)

    data_item = g.db_session.query(DataItem).filter_by(job_id=job_id, data_url=params['url']).first()
    if data_item == None:
        return json_response({'errors': ['Data item not found']}, status=404)

    if params['status'] == 'started':
        params = request.get_json()
        data_item.transfer_started_at = datetime.fromtimestamp(params['current_time'])
        data_item.status = 'in_progress'
    elif params['status'] == 'finished':
        params = request.get_json()
        data_item.transfer_finished_at = datetime.fromtimestamp(params['current_time'])
        data_item.measured_transfer_time = params['measured_transfer_time']
        try:
            data_item.error_message = params['error']
            data_item.status = 'failed'
        except KeyError:
            data_item.transfer_size = params['transfer_size']
            data_item.status = 'completed'
    else:
        return json_response({'errors': ['Invalid status']}, status=400)

    try:
        g.db_session.commit()
        return json_response(True)
    except ValueError as e:
        return json_response({'errors': [str(e)]}, status=400)
