import json
import re

from datetime import datetime
from flask import abort, Flask, g, make_response, redirect, render_template, request, Response, url_for
from flask.ext.login import current_user, LoginManager, login_required
from itsdangerous import Signer
from jinja2 import Markup
from paramiko.rsakey import RSAKey
from StringIO import StringIO

from .common import config, db_engine, DBSession
from .models import User, Job, DataItem, SSHKey
from .routes.util import filter_params, json_response

from .routes.auth import auth_routes

app = Flask(__name__)
app.secret_key = config['app']['secret_key']

@app.template_filter('status_label')
def status_label_filter(status):
    label_classes = {
        'pending': 'default',
        'in_progress': 'primary',
        'completed': 'success',
        'failed': 'danger'
    }
    return Markup(u'<span class="label label-%s">%s</span>' % (label_classes[status.lower()], status.capitalize()))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(userid):
    return g.db_session.query(User).filter_by(id=int(userid)).first()

@login_manager.request_loader
def load_user_from_request(self):
    params = request.get_json()

    if params is None:
        return None

    if 'owner' in params.keys() and 'job_id' in params.keys() and 'signature' in params.keys():
        signer = Signer(config['app']['secret_key'])
        s = '{0},{1}'.format(params['owner'], params['job_id'])
        if signer.unsign('{0}.{1}'.format(s, params['signature'])) == s:
            return g.db_session.query(User).filter_by(email=params['owner']).first()

    return None

@login_manager.unauthorized_handler
def unauthorized():
    if 'content-type' in request.headers.keys() and request.headers['content-type'] == 'application/json':
        return json_response({}, 401)
    else:
        return redirect('/signin')

@app.before_request
def open_db_connection():
    g.db_connection = db_engine.connect()
    g.db_session = DBSession(bind=g.db_connection)

@app.teardown_request
def close_db_connection(exception):
    g.db_session.close()
    g.db_connection.close()

app.register_blueprint(auth_routes)

@app.route('/')
@login_required
def index():
    return redirect('/jobs')

@app.route('/jobs')
@login_required
def jobs_index():
    jobs = g.db_session.query(Job).filter_by(owner=current_user).all()
    return render_template('index.html.jinja', jobs=jobs)

@app.route('/jobs/<job_id>')
@login_required
def show_job_page(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    if job == None:
        abort(404)
    elif job.owner != current_user:
        abort(403)
    else:
        return render_template('show.html.jinja', job=job)

@app.route('/submit')
@login_required
def submit_page():
    transfer_methods = [{'id': id, 'label': method.get('label', id), 'description': method.get('description', None), 'options': method.get('options', None)} for (id, method) in config['data_transfer_methods'].iteritems()]

    destinations = [{'id': id, 'label': dest.get('label', id), 'description': dest.get('description', None)} for (id, dest) in config['data_destinations'].iteritems()]

    return render_template('submit.html.jinja', transfer_methods=transfer_methods, destinations=destinations)

@app.route('/api/jobs', methods=['GET'])
@login_required
def list_jobs():
    jobs = g.db_session.query(Job).filter_by(owner=current_user).all()
    return json_response({'jobs': [job.serialize() for job in jobs]})

@app.route('/api/jobs', methods=['POST'])
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

@app.route('/api/jobs/<job_id>')
@login_required
def show_job(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()

    if job == None:
        abort(404)
    elif job.owner != current_user:
        abort(403)
    else:
        return json_response({'job': job.serialize()})

@app.route('/api/jobs/<job_id>', methods=['POST'])
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

@app.route('/api/jobs/<job_id>/data/status', methods=['POST'])
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

# ========================================================================
# SSH Keys
# ========================================================================

@app.route('/keys', methods=['GET'])
@login_required
def list_keys():
    keys = g.db_session.query(SSHKey).filter_by(owner=current_user).all()
    destinations = [{'id': id, 'label': dest.get('label', id), 'description': dest.get('description', None)} for (id, dest) in config['data_destinations'].iteritems()]
    return render_template('keys_index.html.jinja', keys=keys, destinations=destinations)

@app.route('/keys', methods=['POST'])
@login_required
def create_key():

    username = request.form.get('username')
    destination = request.form.get('destination')

    if not username or not destination:
        return list_keys()

    k = RSAKey.generate(2048)
    out = StringIO()
    k.write_private_key(out)

    key = SSHKey(owner=current_user, username=username, destination=destination)
    comment = "bdss_{email}_{destination}".format(email=current_user.email, destination=destination)
    key.public = "{type} {key} {comment}\n".format(type=k.get_name(), key=k.get_base64(), comment=comment)
    key.private = out.getvalue()

    g.db_session.add(key)
    g.db_session.commit()

    return list_keys()

@app.route('/keys/<key_id>', methods=['GET'])
@login_required
def get_key(key_id):

    key = g.db_session.query(SSHKey).filter_by(owner=current_user, id=key_id).first()

    if key is None:
        app.abort(404)

    response = make_response(key.public)

    filename = 'bdss_' + key.destination + '_id_rsa.pub'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response
