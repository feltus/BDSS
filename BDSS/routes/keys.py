from flask import abort, Blueprint, g, make_response, render_template, request
from flask.ext.login import current_user, login_required
from paramiko.rsakey import RSAKey
from StringIO import StringIO

from ..common import config
from ..models import SSHKey

key_routes = Blueprint('keys', __name__)

@key_routes.route('', methods=['GET'])
@login_required
def list_keys():
    keys = g.db_session.query(SSHKey).filter_by(owner=current_user).all()
    destinations = [{'id': id, 'label': dest.get('label', id), 'description': dest.get('description', None)} for (id, dest) in config['data_destinations'].iteritems()]
    return render_template('keys/index.html.jinja', keys=keys, destinations=destinations)

@key_routes.route('', methods=['POST'])
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
