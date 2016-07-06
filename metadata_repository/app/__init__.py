# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask.ext.login import LoginManager
from htmlmin.minify import html_minify

from .config import secret_key
from .models import db_session, User
from .routes import auth_routes, core_routes, data_source_routes, \
    matcher_routes, test_file_routes, timing_report_routes, transform_routes, \
    user_routes

app = Flask(__name__)
app.secret_key = secret_key


@app.template_filter("format_number")
def format_number(value):
    if isinstance(value, int):
        return "{:,d}".format(value)
    else:
        return "{:,.3f}".format(value)


@app.after_request
def minify_response(response):
    if "text/html" in response.content_type:
        response.set_data(html_minify(response.get_data(as_text=True)))
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Close DB session when app shuts down
    http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
    """
    db_session.remove()


@app.errorhandler(404)
def not_found(error):
    return render_template("errors/not_found.html.jinja"), 404


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.user_id == int(user_id)).first()


@login_manager.unauthorized_handler
def unauthorized():
    if "content-type" in request.headers.keys() and request.headers["content-type"] == "application/json":
        response = jsonify(status="unauthorized")
        response.status_code = 401
        return response
    else:
        return redirect(url_for("auth.login"))


app.register_blueprint(auth_routes)
app.register_blueprint(core_routes)
app.register_blueprint(data_source_routes)
app.register_blueprint(matcher_routes)
app.register_blueprint(test_file_routes)
app.register_blueprint(timing_report_routes)
app.register_blueprint(transform_routes)
app.register_blueprint(user_routes)
