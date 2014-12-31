from flask import abort, Blueprint, g, make_response, render_template, request
from flask.ext.login import current_user, login_required
from paramiko.rsakey import RSAKey
from StringIO import StringIO

from ..common import config
from ..models import SSHKey
from .util import filter_params, json_response

key_routes = Blueprint('keys', __name__)

@key_routes.route('', methods=['GET'])
@login_required
def list_keys():
    keys = g.db_session.query(SSHKey).filter_by(owner=current_user).all()
    destinations = [{'id': id, 'label': dest.get('label', id), 'description': dest.get('description', None)} for (id, dest) in config['data_destinations'].iteritems() if dest['requires_ssh_key']]
    return render_template('keys/index.html.jinja', keys=keys, destinations=destinations)

@key_routes.route('', methods=['POST'])
@login_required
def create_key():
    params = filter_params(request.get_json(), ['username', 'destination'])

    errors = {}
    if 'username' not in params.keys() or len(params['username']) == 0:
        errors['username'] = 'A username is required'

    if not config['data_destinations'][params['destination']]['requires_ssh_key']:
        errors['destination'] = 'This destination does not require an SSH key'

    else:
        # Prevent duplicate keys for a destination.
        key = g.db_session.query(SSHKey).filter_by(owner=current_user, destination=params['destination']).first()
        if key is not None:
            errors['destination'] = 'You already have a key for this destination'

    if errors:
        return json_response({'field_errors': errors}, status=400)

    k = RSAKey.generate(2048)
    out = StringIO()
    k.write_private_key(out)

    key = SSHKey(**params)
    key.owner = current_user
    comment = "bdss_{email}_{destination}".format(email=current_user.email, destination=key.destination)
    key.public = "{type} {key} {comment}\n".format(type=k.get_name(), key=k.get_base64(), comment=comment)
    key.private = out.getvalue()

    g.db_session.add(key)
    g.db_session.commit()

    return json_response({}, status=201)

@key_routes.route('/<key_id>', methods=['GET'])
@login_required
def get_key(key_id):

    key = g.db_session.query(SSHKey).filter_by(owner=current_user, id=key_id).first()

    if key is None:
        app.abort(404)

    response = make_response(key.public)

    filename = 'bdss_' + key.destination + '_id_rsa.pub'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response
