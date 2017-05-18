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

from flask import abort, Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from .auth import admin_required
from ..forms import ConfirmDeleteForm, UrlMatcherForm
from ..forms.subform_handling import process_form_with_options_subform, render_options_subform
from ..models import db_session, DataSource, UrlMatcher
from ..util import available_matcher_types, options_form_class_for_matcher_type, render_matcher_description


routes = Blueprint("matchers", __name__)


@routes.route("/data_sources/<source_id>/matchers")
def list_url_matchers(source_id):
    """
    List matcher descriptions for a data source.
    """
    if "Accept" not in request.headers or "application/json" not in request.headers["Accept"]:
        return redirect(url_for("data_sources.show_data_source", source_id=source_id))

    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    descriptions = [render_matcher_description(m.matcher_type, m.matcher_options) for m in data_source.url_matchers]
    return jsonify(matchers=descriptions)


@routes.route("/data_sources/<source_id>/matchers/new", methods=["GET", "POST"])
@login_required
@admin_required
def add_url_matcher(source_id):
    """
    Add a new URL matcher to a data source
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    form = process_form_with_options_subform(UrlMatcherForm,
                                             "matcher_type", "matcher_options",
                                             options_form_class_for_matcher_type)

    if request.method == "POST" and form.validate():
        url_matcher = UrlMatcher(
            data_source_id=data_source.id,
            matcher_id=len(data_source.url_matchers) + 1,
            matcher_type=form.matcher_type.data
        )
        if "matcher_options" in form._fields.keys() and form._fields["matcher_options"]:
            url_matcher.matcher_options = form._fields["matcher_options"].data
        else:
            url_matcher.matcher_options = {}

        try:
            db_session.add(url_matcher)
            db_session.commit()
            flash("Matcher saved", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to save matcher", "danger")
            traceback.print_exc()

    return render_template("url_matchers/new.html.jinja", data_source=data_source, form=form)


@routes.route("/data_sources/<source_id>/matchers/<matcher_id>")
def show_url_matcher(source_id, matcher_id):
    """
    Show information about a specific matcher.
    """
    url_matcher = UrlMatcher.query.filter((UrlMatcher.data_source_id == source_id) & (UrlMatcher.matcher_id == matcher_id)).first() or abort(404)

    return render_template("url_matchers/show.html.jinja", data_source=url_matcher.data_source, url_matcher=url_matcher,
                           render_matcher_description=render_matcher_description)


@routes.route("/data_sources/<source_id>/matchers/<matcher_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_url_matcher(source_id, matcher_id):
    """
    Edit a matcher
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    url_matcher = UrlMatcher.query.filter((UrlMatcher.data_source_id == source_id) & (UrlMatcher.matcher_id == matcher_id)).first() or abort(404)

    form = process_form_with_options_subform(UrlMatcherForm,
                                             "matcher_type", "matcher_options",
                                             options_form_class_for_matcher_type,
                                             editing_obj=url_matcher)

    if request.method == "POST" and form.validate():
        url_matcher.matcher_type = form.matcher_type.data
        if "matcher_options" in form._fields.keys() and form._fields["matcher_options"]:
            url_matcher.matcher_options = form._fields["matcher_options"].data
        else:
            url_matcher.matcher_options = {}

        try:
            db_session.commit()
            flash("Matcher updated", "success")
            return redirect(url_for("matchers.show_url_matcher", source_id=data_source.id, matcher_id=url_matcher.matcher_id))
        except:
            db_session.rollback()
            flash("Failed to update matcher", "danger")
            traceback.print_exc()

    return render_template("url_matchers/edit.html.jinja", data_source=data_source, url_matcher=url_matcher, form=form)


@routes.route("/data_sources/<source_id>/matchers/<matcher_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_url_matcher(source_id, matcher_id):
    """
    Delete a URL matcher. Prompt for confirmation first.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    url_matcher = UrlMatcher.query.filter((UrlMatcher.data_source_id == source_id) & (UrlMatcher.matcher_id == matcher_id)).first() or abort(404)
    form = ConfirmDeleteForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(url_matcher)
            db_session.commit()
            flash("Matcher deleted", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to delete matcher", "danger")
            traceback.print_exc()

    return render_template("url_matchers/delete.html.jinja", data_source=data_source, form=form, url_matcher=url_matcher)


@routes.route("/data_sources/matcher_options_form")
@login_required
@admin_required
def show_matcher_options_form():
    """Show options form for a specific matcher type."""
    return render_options_subform(
        available_matcher_types(),
        options_form_class_for_matcher_type,
        "matcher_options")
