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
import wtforms

from flask import abort, Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from .auth import admin_required
from ..forms import ConfirmDeleteForm, DestinationForm
from ..forms.validators import Unique
from ..models import db_session, Destination


routes = Blueprint("destinations", __name__)


@routes.route("/destinations")
def list_destinations():
    """
    List all destinations in database.
    """
    if "application/json" in request.headers["Accept"]:
        destinations = Destination.query.all()
        return jsonify(destinations=[{"id": d.id, "label": d.label} for d in destinations])

    page_num = int(request.args.get("page", 1))
    num_per_page = 10
    destinations = Destination.query.limit(num_per_page).offset((page_num - 1) * num_per_page).all()
    total_num = Destination.query.count()
    total_num_pages = math.ceil(total_num / num_per_page)
    page_range = range(max(1, page_num - 3), min(total_num_pages, page_num + 3) + 1)
    return render_template("destinations/index.html.jinja", destinations=destinations, page_num=page_num,
                           page_range=page_range, total_num_pages=total_num_pages)


@routes.route("/destinations/new", methods=["GET", "POST"])
@login_required
@admin_required
def create_destination():
    """
    Add a new destination to the database.
    """
    form = DestinationForm(request.form)

    if request.method == "POST" and form.validate():
        destination = Destination()
        form.populate_obj(destination)

        try:
            db_session.add(destination)
            db_session.commit()
            flash("Destination saved", "success")
            return redirect(url_for("destinations.show_destination", destination_id=destination.id))
        except:
            db_session.rollback()
            flash("Failed to save destination", "danger")
            traceback.print_exc()

    return render_template("destinations/new.html.jinja", form=form)


@routes.route("/destinations/<destination_id>")
@login_required
def show_destination(destination_id):
    """
    Show information about a specific destination.
    """
    destination = Destination.query.filter(Destination.id == destination_id).first() or abort(404)
    return render_template("destinations/show.html.jinja", destination=destination)


@routes.route("/destinations/<destination_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_destination(destination_id):
    """
    For GET requests, show form for editing a destination.
    For POST requests, process form and update destination in database.
    """
    destination = Destination.query.filter(Destination.id == destination_id).first() or abort(404)
    form = DestinationForm(request.form, destination)
    label_validators = [wtforms.validators.InputRequired(), Unique(Destination, "label", lambda q: q.filter(Destination.id != destination_id))]
    setattr(form.label, "validators", label_validators)

    if request.method == "POST" and form.validate():
        form.populate_obj(destination)

        try:
            db_session.commit()
            flash("Destination updated", "success")
            return redirect(url_for("destinations.show_destination", destination_id=destination_id))
        except:
            db_session.rollback()
            flash("Failed to update destination", "danger")
            traceback.print_exc()

    return render_template("destinations/edit.html.jinja", destination=destination, form=form)


@routes.route("/destinations/<destination_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_destination(destination_id):
    destination = Destination.query.filter(Destination.id == destination_id).first()
    form = ConfirmDeleteForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(destination)
            db_session.commit()
            flash("Destination deleted", "success")
            return redirect(url_for("destinations.list_destinations"))
        except:
            db_session.rollback()
            flash("Failed to delete destination", "danger")
            traceback.print_exc()

    return render_template("destinations/delete.html.jinja", destination=destination, form=form)
