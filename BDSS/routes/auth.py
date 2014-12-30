import re

from flask import Blueprint, g, redirect, render_template, request
from flask.ext.login import login_required, login_user, logout_user
from passlib.context import CryptContext

from ..models import User
from .util import json_response

auth_routes = Blueprint('auth', __name__)

pwd_context = CryptContext(schemes='bcrypt_sha256')

@auth_routes.route('/signin', methods=['GET'])
def signin_page():
    return render_template('auth/signin.html.jinja')

@auth_routes.route('/signin', methods=['POST'])
def signin():
    params = request.get_json()

    errors = {}

    if 'email' not in params.keys() or len(params['email']) == 0:
        errors['email'] = 'A valid email address is required'

    if 'password' not in params.keys() or len(params['password']) == 0:
        errors['password'] = 'A password is required'

    if len(errors) > 0:
        return json_response({'field_errors': errors}, status=400)
    else:
        user = g.db_session.query(User).filter_by(email=params['email']).first()
        if user and pwd_context.verify(params['password'], user.password_hash):
            login_user(user)
            return json_response({})
        else:
            return json_response({'field_errors': {'password': 'Invalid username/password combination'}}, status=401)

@auth_routes.route('/signup', methods=['GET'])
def signup_page():
    return render_template('auth/signup.html.jinja')

@auth_routes.route('/signup', methods=['POST'])
def signup():
    params = request.get_json()

    errors = {}

    if 'name' not in params.keys() or len(params['name']) == 0:
        errors['name'] = 'A name is required'

    if 'email' not in params.keys() or len(params['email']) == 0 or not re.compile(r'^\S+@.+\.\S+$').match(params['email']):
        errors['email'] = 'A valid email address is required'
    else:
        user = g.db_session.query(User).filter_by(email=params['email']).first()
        if user:
            errors['email'] = 'This email address is already in use'

    if 'password' not in params.keys() or len(params['password']) == 0:
        errors['password'] = 'A password is required'
    elif len(params['password']) < 6:
        errors['password'] = 'Your password must be at least 6 characters long'
    elif 'password_confirmation' not in params.keys() or len(params['password_confirmation']) == 0:
        errors['password_confirmation'] = 'You must confirm your password'
    elif params['password'] != params['password_confirmation']:
        errors['password_confirmation'] = 'Password confirmation does not match password'

    if len(errors) > 0:
        return json_response({'field_errors': errors}, status=400)
    else:
        pwd_hash = pwd_context.encrypt(params['password'])
        user = User(name=params['name'], email=params['email'], password_hash=pwd_hash)
        g.db_session.add(user)
        g.db_session.commit()
        login_user(user)
        return json_response({})

@auth_routes.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect('/signin')
