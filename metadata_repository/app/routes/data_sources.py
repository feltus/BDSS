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

from flask import abort, Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func
from wtforms import validators

from .auth import admin_required
from ..forms import ConfirmDeleteForm, DataSourceForm, DataSourceSearchForm, UrlForm
from ..forms.subform_handling import process_form_with_options_subform, render_options_subform
from ..forms.validators import Unique
from ..models import db_session, DataSource
from ..util import render_matcher_description, render_transform_description, \
    available_transfer_mechanism_types, options_form_class_for_transfer_mechanism_type


routes = Blueprint("data_sources", __name__)


@routes.route("/data_sources")
@login_required
def list_data_sources():
    """
    List all data sources in database.
    """
    page_num = int(request.args.get("page", 1))
    num_sources_per_page = 10
    data_sources = DataSource.query.limit(num_sources_per_page).offset((page_num - 1) * num_sources_per_page).all()
    total_num_sources = DataSource.query.count()
    total_num_pages = math.ceil(total_num_sources / num_sources_per_page)
    page_range = range(max(1, page_num - 3), min(total_num_pages, page_num + 3) + 1)
    return render_template("data_sources/index.html.jinja", data_sources=data_sources, page_num=page_num,
                           page_range=page_range, total_num_pages=total_num_pages)


@routes.route("/data_sources/new", methods=["GET", "POST"])
@login_required
@admin_required
def create_data_source():
    """
    Add a new data source to the database.
    """
    form = process_form_with_options_subform(DataSourceForm,
                                             "transfer_mechanism_type", "transfer_mechanism_options",
                                             options_form_class_for_transfer_mechanism_type)

    if request.method == "POST" and form.validate():
        source = DataSource(
            label=form.label.data,
            description=form.description.data,
            transfer_mechanism_type=form.transfer_mechanism_type.data
        )
        if "transfer_mechanism_options" in form._fields.keys() and form._fields["transfer_mechanism_options"]:
            source.transfer_mechanism_options = form._fields["transfer_mechanism_options"].data
        else:
            source.transfer_mechanism_options = {}

        try:
            db_session.add(source)
            db_session.commit()
            flash("Data source saved", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=source.id))
        except:
            db_session.rollback()
            flash("Failed to save data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/new.html.jinja", form=form)


@routes.route("/data_sources/<source_id>")
@login_required
def show_data_source(source_id):
    """
    Show information about a specific data source.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    return render_template("data_sources/show.html.jinja", data_source=data_source,
                           render_matcher_description=render_matcher_description,
                           render_transform_description=render_transform_description)


@routes.route("/data_sources/<source_id>/test_match", methods=["GET", "POST"])
@login_required
def test_data_source_url_match(source_id):
    """
    Test whether or not a URL matches a data source.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    form = UrlForm(request.form)

    if request.method == "POST" and form.validate():
        if data_source.matches_url(form.url.data):
            flash("URL matches", "success")
        else:
            flash("URL does not match", "danger")

    return render_template("data_sources/test_url.html.jinja", data_source=data_source, form=form)


@routes.route("/data_sources/<source_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_data_source(source_id):
    """
    For GET requests, show form for editing a data source.
    For POST requests, process form and update data source in database.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    label_validators = [validators.InputRequired(), Unique(DataSource, "label", lambda q: q.filter(DataSource.id != source_id))]
    form = process_form_with_options_subform(DataSourceForm,
                                             "transfer_mechanism_type", "transfer_mechanism_options",
                                             options_form_class_for_transfer_mechanism_type,
                                             editing_obj=data_source,
                                             form_init=lambda f: setattr(f.label, "validators", label_validators))

    if request.method == "POST" and form.validate():
        data_source.label = form.label.data
        data_source.description = form.description.data
        data_source.transfer_mechanism_type = form.transfer_mechanism_type.data
        if "transfer_mechanism_options" in form._fields.keys() and form._fields["transfer_mechanism_options"]:
            data_source.transfer_mechanism_options = form._fields["transfer_mechanism_options"].data
        else:
            data_source.transfer_mechanism_options = {}

        try:
            db_session.commit()
            flash("Data source updated", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=source_id))
        except:
            db_session.rollback()
            flash("Failed to update data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/edit.html.jinja", data_source=data_source, form=form)


@routes.route("/data_sources/<source_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_data_source(source_id):
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    form = ConfirmDeleteForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(data_source)
            db_session.commit()
            flash("Data source deleted", "success")
            return redirect(url_for("data_sources.list_data_sources"))
        except:
            db_session.rollback()
            flash("Failed to delete data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/delete.html.jinja", data_source=data_source, form=form)


@routes.route("/data_sources/transfer_mechanism_options_form")
@login_required
@admin_required
def show_transfer_mechanism_options_form():
    """Show options form for a specific transfer mechanism type."""
    return render_options_subform(
        available_transfer_mechanism_types(),
        options_form_class_for_transfer_mechanism_type,
        "transfer_mechanism_options")


@routes.route("/data_sources/relations")
def data_source_relations():
    data_sources = DataSource.query.all()
    nodes = []
    links = []
    for ds in data_sources:
        nodes.append({"id": ds.id, "label": ds.label})
        for t in ds.transforms:
            links.append({"source": ds.id, "target": t.to_data_source_id})

    return render_template("data_sources/links.html.jinja", nodes=nodes, links=links)


@routes.route("/data_sources/search")
def search_data_sources():
    form = DataSourceSearchForm(q=request.args.get("q"))

    if form.validate():
        data_sources = DataSource.query.filter(func.lower(DataSource.label).like("%%%s%%" % form.q.data.lower())).all()

        if "application/json" in request.headers.getlist("Accept"):
            return jsonify(data_sources=[{"id": d.id, "label": d.label} for d in data_sources])
        else:
            return render_template("data_sources/search_results.html.jinja", data_sources=data_sources, form=form)
    else:
        if "application/json" in request.headers.getlist("Accept"):
            abort(400)
        else:
            return render_template("data_sources/search_results.html.jinja", data_sources=None, form=form)
