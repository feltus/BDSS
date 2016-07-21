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

from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from .auth import admin_required
from ..forms import ConfirmDeleteForm, UrlTransformForm
from ..forms.subform_handling import process_form_with_options_subform, render_options_subform
from ..models import db_session, DataSource, Destination, Transform
from ..util import available_transform_types, options_form_class_for_transform_type, render_transform_description


routes = Blueprint("transforms", __name__)


def _setup_transform_form(from_data_source_id):
    data_sources = DataSource.query.filter(DataSource.id != from_data_source_id).all()
    c1 = [(src.id, src.label) for src in data_sources]

    destinations = Destination.query.all()
    c2 = [(d.id, d.label) for d in destinations]

    def setup_form(form):
        setattr(form.to_data_source_id, "choices", c1)
        setattr(form.for_destination_ids, "choices", c2)

    return setup_form


@routes.route("/data_sources/<source_id>/transforms/new", methods=["GET", "POST"])
@login_required
@admin_required
def add_transform(source_id):
    """
    Add a new URL transform to a data source
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    form = process_form_with_options_subform(UrlTransformForm,
                                             "transform_type", "transform_options",
                                             options_form_class_for_transform_type,
                                             form_init=_setup_transform_form(source_id))

    if request.method == "POST" and form.validate():
        transform = Transform(
            from_data_source_id=data_source.id,
            to_data_source_id=form.to_data_source_id.data,
            transform_id=len(data_source.transforms) + 1,
            transform_type=form.transform_type.data,
            description=form.description.data,
            preference_order=max([s.preference_order for s in data_source.transforms] + [-1]) + 1
        )
        if form.for_destination_ids.data:
            transform.for_destinations = Destination.query.filter(Destination.id.in_(form.for_destination_ids.data)).all()
        else:
            transform.for_destinations = []
        if "transform_options" in form._fields.keys() and form._fields["transform_options"]:
            transform.transform_options = form._fields["transform_options"].data
        else:
            transform.transform_options = {}

        try:
            db_session.add(transform)
            db_session.commit()
            flash("Transform saved", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to save transform", "danger")
            traceback.print_exc()

    return render_template("transforms/new.html.jinja", from_data_source=data_source, form=form)


@routes.route("/data_sources/<source_id>/transforms/<transform_id>")
@login_required
def show_transform(source_id, transform_id):
    """
    Show information about a specific transform.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    transform = Transform.query.filter((Transform.from_data_source_id == source_id) & (Transform.transform_id == transform_id)).first() or abort(404)

    return render_template("transforms/show.html.jinja", from_data_source=data_source, transform=transform,
                           render_transform_description=render_transform_description)


@routes.route("/data_sources/<source_id>/transforms/<transform_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_transform(source_id, transform_id):
    """
    Edit a transform
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    transform = Transform.query.filter((Transform.from_data_source_id == source_id) & (Transform.transform_id == transform_id)).first() or abort(404)

    form = process_form_with_options_subform(UrlTransformForm,
                                             "transform_type", "transform_options",
                                             options_form_class_for_transform_type,
                                             editing_obj=transform,
                                             form_init=_setup_transform_form(source_id))

    if request.method == "POST" and form.validate():
        transform.to_data_source_id = form.to_data_source_id.data
        transform.transform_type = form.transform_type.data
        transform.description = form.description.data
        if form.for_destination_ids.data:
            transform.for_destinations = Destination.query.filter(Destination.id.in_(form.for_destination_ids.data)).all()
        else:
            transform.for_destinations = []
        if "transform_options" in form._fields.keys() and form._fields["transform_options"]:
            transform.transform_options = form._fields["transform_options"].data
        else:
            transform.transform_options = {}

        try:
            db_session.commit()
            flash("Transform updated", "success")
            return redirect(url_for("transforms.show_transform", source_id=data_source.id, transform_id=transform.transform_id))
        except:
            db_session.rollback()
            flash("Failed to update transform", "danger")
            traceback.print_exc()

    return render_template("transforms/edit.html.jinja", from_data_source=data_source, transform=transform, form=form)


@routes.route("/data_sources/<source_id>/transforms/<transform_id>/reorder")
@login_required
@admin_required
def edit_transform_order(source_id, transform_id):
    direction = request.args.get("direction")

    if direction not in ["up", "down"]:
        flash("Invalid direction", "danger")
        return redirect(url_for("data_sources.show_data_source", source_id=source_id))

    transform = Transform.query.filter((DataSource.id == source_id) & (Transform.transform_id == transform_id)).first() or abort(404)
    ds = transform.from_data_source
    if direction == "up":
        if transform.preference_order == min([s.preference_order for s in ds.transforms]):
            flash("Transform already first for this source", "danger")
            return redirect(url_for("data_sources.show_data_source", source_id=source_id))
        else:
            prev_transform = [t for t in ds.transforms if t.preference_order < transform.preference_order][-1]
            prev_transform.preference_order, transform.preference_order = transform.preference_order, prev_transform.preference_order

    elif direction == "down":
        if transform.preference_order == max([s.preference_order for s in ds.transforms]):
            flash("Transform already last for this source", "danger")
            return redirect(url_for("data_sources.show_data_source", source_id=source_id))
        else:
            next_transform = [t for t in ds.transforms if t.preference_order > transform.preference_order][0]
            next_transform.preference_order, transform.preference_order = transform.preference_order, next_transform.preference_order

    try:
        db_session.commit()
        flash("Transforms reordered", "success")
    except:
        db_session.rollback()
        flash("Failed to reorder transforms", "danger")
        traceback.print_exc()

    return redirect(url_for("data_sources.show_data_source", source_id=source_id))


@routes.route("/data_sources/<source_id>/transforms/<transform_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_transform(source_id, transform_id):
    """
    Delete a URL transform. Prompt for confirmation first.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    transform = Transform.query.filter((Transform.from_data_source_id == source_id) & (Transform.transform_id == transform_id)).first() or abort(404)
    form = ConfirmDeleteForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(transform)
            db_session.commit()
            flash("Transform deleted", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to delete transform", "danger")
            traceback.print_exc()

    return render_template("transforms/delete.html.jinja", form=form, from_data_source=data_source, transform=transform)


@routes.route("/data_sources/transform_options_form")
@login_required
@admin_required
def show_transform_options_form():
    """Show options form for a specific transform type."""
    return render_options_subform(
        available_transform_types(),
        options_form_class_for_transform_type,
        "transform_options")
