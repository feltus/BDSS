import json
import re

from datetime import datetime
from flask import abort, Flask, g, redirect, render_template, request, Response, url_for
from flask.ext.login import current_user, LoginManager, login_required, login_user, logout_user
from jinja2 import Markup
from passlib.context import CryptContext

from .common import config, db_engine, DBSession
from .models import User, Job, DataItem


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

@login_manager.unauthorized_handler
def unauthorized():
    if 'content-type' in request.headers.keys() and request.headers['content-type'] == 'application/json':
        return json_response({}, 401)
    else:
        return redirect('/signin')

pwd_context = CryptContext(schemes='bcrypt_sha256')

@app.before_request
def open_db_connection():
    g.db_connection = db_engine.connect()
    g.db_session = DBSession(bind=g.db_connection)

@app.teardown_request
def close_db_connection(exception):
    g.db_session.close()
    g.db_connection.close()

@app.route('/')
@login_required
def index():
    return redirect('/jobs')

@app.route('/signin', methods=['GET'])
def signin_page():
    return render_template('signin.html.jinja')

@app.route('/signin', methods=['POST'])
def signin():
    params = request.get_json()

    errors = {}

    if 'email' not in params.keys() or len(params['email']) == 0:
        errors['email'] = 'A valid email address is required'

    if 'password' not in params.keys() or len(params['password']) == 0:
        errors['password'] = 'A password is required'

    if len(errors) > 0:
        return json_response({'errors': errors}, status=400)
    else:
        user = g.db_session.query(User).filter_by(email=params['email']).first()
        if user and pwd_context.verify(params['password'], user.password_hash):
            login_user(user)
            return json_response({})
        else:
            return json_response({'errors': {'password': 'Invalid username/password combination'}}, status=401)

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html.jinja')

@app.route('/signup', methods=['POST'])
def signup():
    params = request.get_json()

    errors = {}

    if 'name' not in params.keys() or len(params['name']) == 0:
        errors['name'] = 'A name is required'

    if 'email' not in params.keys() or len(params['email']) == 0 or not re.compile(r'^\S+@.+\.\S+$').match(params['email']):
        errors['email'] = 'A valid email address is required'

    if 'password' not in params.keys() or len(params['password']) == 0:
        errors['password'] = 'A password is required'
    elif len(params['password']) < 6:
        errors['password'] = 'Your password must be at least 6 characters long'
    elif 'password_confirmation' not in params.keys() or len(params['password_confirmation']) == 0:
        errors['password_confirmation'] = 'You must confirm your password'
    elif params['password'] != params['password_confirmation']:
        errors['password_confirmation'] = 'Password confirmation does not match password'

    if len(errors) > 0:
        return json_response({'errors': errors}, status=400)
    else:
        pwd_hash = pwd_context.encrypt(params['password'])
        user = User(name=params['name'], email=params['email'], password_hash=pwd_hash)
        g.db_session.add(user)
        g.db_session.commit()
        login_user(user)
        return json_response({})

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect('/signin')

@app.route('/jobs')
@login_required
def jobs_index():
    jobs = g.db_session.query(Job).all()
    return render_template('index.html.jinja', jobs=jobs)

@app.route('/jobs/<job_id>')
@login_required
def show_job_page(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    if job == None:
        abort(404)
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
    return json_response({'jobs': [job.serialize() for job in g.db_session.query(Job).all()]})

@app.route('/api/jobs', methods=['POST'])
@login_required
def create_job():
    params = request.get_json()

    job_params = filter_params(params['job'], ['name', 'email', 'data_transfer_method', 'data_transfer_method_options', 'data_destination', 'destination_directory'])

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

@app.route('/api/jobs/<job_id>')
@login_required
def show_job(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()

    if job != None:
        return json_response({'job': job.serialize()})
    else:
        return json_response({}, status=404)

@app.route('/api/jobs/<job_id>', methods=['POST'])
@login_required
def update_job(job_id):
    job = g.db_session.query(Job).filter_by(job_id=job_id).first()
    params = request.get_json()

    if job != None:
        job.measured_time = params['measured_time']
        g.db_session.commit()
        return json_response({'job': job.serialize()})
    else:
        return json_response({}, status=404)

@app.route('/api/jobs/<job_id>/data/status', methods=['POST'])
@login_required
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
            data_item.transfer_size = params['transfer_size']
            data_item.status = 'completed'
    else:
        return json_response({'errors': ['Invalid status']}, status=400)

    try:
        g.db_session.commit()
        return json_response(True)
    except ValueError as e:
        return json_response({'errors': [str(e)]}, status=400)
