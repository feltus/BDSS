from flask import Flask, g, redirect, request
from flask.ext.login import LoginManager, login_required
from itsdangerous import Signer
from jinja2 import Markup

from .common import config, db_engine, DBSession
from .models import Job, User
from .routes.util import json_response

from .routes.auth import auth_routes
from .routes.jobs import job_routes
from .routes.keys import key_routes

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
    return Markup(u'<span class="label label-%s">%s</span>' % (label_classes[status.lower()], status.replace('_', ' ').capitalize()))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(userid):
    return g.db_session.query(User).filter_by(id=int(userid)).first()

@login_manager.request_loader
def load_user_from_request(self):

    if request.endpoint == 'jobs.update_job' or request.endpoint == 'jobs.update_transfer_status':
        auth = request.headers.get('Authorization')
        token = auth.split(' ')[1]

        job = g.db_session.query(Job).filter_by(reporting_token=token).first()
        if job:
            return job.owner

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
app.register_blueprint(job_routes, url_prefix='/jobs')
app.register_blueprint(key_routes, url_prefix='/keys')

@app.route('/')
@login_required
def index():
    return redirect('/jobs')
