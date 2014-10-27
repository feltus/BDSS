import json

from datetime import datetime
from flask import Flask, g, request, Response

from .common import config, db_engine, DBSession
from .models import Job, DataItem


## Filter request params to prevent mass assignment.
#  @param params Dictionary containing request params.
#  @param allowed_keys Collection of keys.
#  @return Dictionary containing only the values of params whose keys are
#   present in allowed_keys.
def filter_params(params, allowed_keys):
    return {k:v for (k, v) in params.iteritems() if k in allowed_keys}

## Create a Flask response containing JSON output.
def json_response(obj, status=200):
    return Response(json.dumps(obj), status=status, mimetype='application/json')


app = Flask(__name__)


@app.before_request
def open_db_connection():
    g.db_connection = db_engine.connect()
    g.db_session = DBSession(bind=g.db_connection)

@app.teardown_request
def close_db_connection(exception):
    g.db_session.close()
    g.db_connection.close()


@app.route('/jobs', methods=['GET'])
def list_jobs():
    return json_response({'jobs': [job.serialize() for job in g.db_session.query(Job).all()]})

@app.route('/jobs', methods=['POST'])
def create_job():
    params = request.get_json()

    job_params = filter_params(params['job'], ['name', 'email', 'data_transfer_method', 'data_transfer_method_options', 'data_destination'])

    data_params = [filter_params(p, ['data_url', 'checksum', 'checksum_method']) for p in params['job']['required_data']]

    job = Job(**job_params)
    for p in data_params:
        job.required_data.append(DataItem(**p))

    try:
        g.db_session.add(job)
        g.db_session.commit()
        return json_response({'job': job.serialize()}, status=201)
    except ValueError as e:
        g.db_session.rollback()
        return json_response({'errors': [str(e)]}, status=400)

@app.route('/jobs/<job_id>')
def show_job(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()

    if job != None:
        return json_response({'job': job.serialize()})
    else:
        return json_response({}, status=404)

@app.route('/jobs/<job_id>/data/status', methods=['POST'])
def update_transfer_status(job_id):
    params = request.get_json()

    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    if job == None:
        return json_response({'errors': ['Job not found']}, status=404)

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
            data_item.status = 'completed'
    else:
        return json_response({'errors': ['Invalid status']}, status=400)

    try:
        g.db_session.commit()
        return json_response(True)
    except ValueError as e:
        return json_response({'errors': [str(e)]}, status=400)

@app.route('/data_transfer_methods')
def list_data_transfer_methods():
    methods = [dict(method.iteritems(), id=id) for (id, method) in config['data_transfer_methods'].iteritems()]

    return json_response({'methods': sorted(methods, lambda m1,m2: cmp(m1['id'], m2['id']))})

@app.route('/data_destinations')
def list_data_destinations():
    destinations = [{'id': id, 'label': dest['label'], 'description': dest['description']} for (id, dest) in config['data_destinations'].iteritems()]
    return json_response({'destinations': sorted(destinations, lambda d1, d2: cmp(d1['id'], d2['id']))})
