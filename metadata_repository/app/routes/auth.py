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

import traceback
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_app, current_user, login_required, login_user, logout_user

from ..forms import LoginForm, RegistrationForm
from ..models import db_session, User


routes = Blueprint("auth", __name__)


def admin_required(func):
    """
    Decorator to require admin rights to access a route
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in set(["OPTIONS"]):
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_admin:
            return render_template("errors/admin_permission_required.html.jinja"), 403
        return func(*args, **kwargs)
    return decorated_view


@routes.route("/login", methods=["GET", "POST"])
def login():
    """
    Login to the application.
    """
    if current_user and not current_user.is_anonymous:
        return redirect(url_for("core.index"))

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("core.index"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("users/login.html.jinja", form=form)


@routes.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user account.
    """
    if current_user and not current_user.is_anonymous:
        return redirect(url_for("core.index"))

    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db_session.add(user)
            db_session.commit()
            login_user(user, remember=True)
            flash("Registration successful")
            return redirect(url_for("core.index"))
        except:
            db_session.rollback()
            flash("Unable to register", "danger")
            traceback.print_exc()

    return render_template("users/register.html.jinja", form=form)


@login_required
@routes.route("/logout")
def logout():
    """
    Logout of the application.
    """
    logout_user()
    return redirect(url_for("auth.login"))
