from flask import Flask, g, redirect, request
from flask.ext.login import LoginManager, login_required
from itsdangerous import Signer
from jinja2 import Markup

from .common import config, db_engine, DBSession
from .models import User
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
app.register_blueprint(job_routes, url_prefix='/jobs')
app.register_blueprint(key_routes, url_prefix='/keys')

@app.route('/')
@login_required
def index():
    return redirect('/jobs')
