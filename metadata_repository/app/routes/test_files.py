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
from ..forms import ConfirmDeleteForm, TransferTestFileForm
from ..models import db_session, DataSource, TransferTestFile


routes = Blueprint("test_files", __name__)


@routes.route("/data_sources/<source_id>/test_files")
def list_test_files(source_id):
    """
    List test files for a particular data source
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    if request.headers.get("Accept") == "application/json":
        return jsonify(test_files=[f.url for f in data_source.transfer_test_files])
    else:
        return redirect(url_for("data_sources.show_data_source", source_id=source_id))


@routes.route("/data_sources/<source_id>/test_files/new", methods=["GET", "POST"])
@login_required
@admin_required
def add_test_file(source_id):
    """
    Add a new test file to a data source
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    form = TransferTestFileForm(request.form)

    if request.method == "POST" and form.validate():
        test_file = TransferTestFile(
            data_source_id=data_source.id,
            file_id=len(data_source.transfer_test_files) + 1)
        form.populate_obj(test_file)

        if data_source.matches_url(test_file.url):
            try:
                db_session.add(test_file)
                db_session.commit()
                flash("Test file saved", "success")
                return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
            except:
                db_session.rollback()
                flash("Failed to save test file", "danger")
                traceback.print_exc()
        else:
            flash("Test file URL does not match data source", "danger")

    return render_template("test_files/new.html.jinja", data_source=data_source, form=form)


@routes.route("/data_sources/<source_id>/test_files/<file_id>")
def show_test_file(source_id, file_id):
    """
    Show information about a specific test file.
    """
    test_file = TransferTestFile.query.filter((TransferTestFile.data_source_id == source_id) & (TransferTestFile.file_id == file_id)).first() or abort(404)

    return render_template("test_files/show.html.jinja", test_file=test_file)


@routes.route("/data_sources/<source_id>/test_files/<file_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_test_file(source_id, file_id):
    """
    Edit a test file
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    test_file = TransferTestFile.query.filter((TransferTestFile.data_source_id == source_id) & (TransferTestFile.file_id == file_id)).first() or abort(404)
    form = TransferTestFileForm(request.form, test_file)

    if request.method == "POST" and form.validate():
        form.populate_obj(test_file)

        if data_source.matches_url(test_file.url):
            try:
                db_session.commit()
                flash("Test file updated", "success")
                return redirect(url_for("test_files.show_test_file", source_id=data_source.id, file_id=test_file.file_id))
            except:
                db_session.rollback()
                flash("Failed to update test file", "danger")
                traceback.print_exc()
        else:
            flash("Test file URL does not match data source", "danger")

    return render_template("test_files/edit.html.jinja", test_file=test_file, form=form)


@routes.route("/data_sources/<source_id>/test_files/<file_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_test_file(source_id, file_id):
    """
    Delete a test file. Prompt for confirmation first.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)
    test_file = TransferTestFile.query.filter((TransferTestFile.data_source_id == source_id) & (TransferTestFile.file_id == file_id)).first() or abort(404)
    form = ConfirmDeleteForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(test_file)
            db_session.commit()
            flash("Test file deleted", "success")
            return redirect(url_for("data_sources.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to delete test file", "danger")
            traceback.print_exc()

    return render_template("test_files/delete.html.jinja", form=form, test_file=test_file)
