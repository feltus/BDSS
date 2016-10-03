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

import math
import traceback

from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .auth import admin_required
from ..forms import ToggleUserPermissionsForm
from ..models import db_session, User


routes = Blueprint("users", __name__)


@routes.route("/users")
@login_required
@admin_required
def list_users():
    """
    List all users in database
    """
    page_num = int(request.args.get("page", 1))
    num_users_per_page = 10
    users = User.query.order_by(User.is_admin.desc()).order_by(User.name) \
        .limit(num_users_per_page).offset((page_num - 1) * num_users_per_page).all()
    total_num_users = User.query.count()
    total_num_pages = math.ceil(total_num_users / num_users_per_page)
    page_range = range(max(1, page_num - 3), min(total_num_pages, page_num + 3) + 1)
    return render_template("users/index.html.jinja", users=users, page_num=page_num, page_range=page_range,
                           total_num_pages=total_num_pages)


@routes.route("/users/<user_id>")
@login_required
@admin_required
def show_user(user_id):
    """
    Show information about a specific user
    """
    user = User.query.filter(User.user_id == user_id).first() or abort(404)
    return render_template("users/show.html.jinja", user=user)


@routes.route("/users/<user_id>/edit_permissions", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user_permissions(user_id):
    """
    Grant/revoke admin permissions for a user
    """
    user = User.query.filter(User.user_id == user_id).first() or abort(404)
    form = ToggleUserPermissionsForm(request.form)

    if request.method == "POST" and form.validate():
        if user.user_id == current_user.user_id:
            flash("Unable to change your own permissions", "danger")
        else:
            user.is_admin = not user.is_admin
            try:
                db_session.commit()
                flash("Permissions updated", "success")
                return redirect(url_for("users.show_user", user_id=user.user_id))
            except:
                db_session.rollback()
                flash("Failed to update permissions", "danger")
                traceback.print_exc()

    return render_template("users/edit_permissions.html.jinja", form=form, user=user)
