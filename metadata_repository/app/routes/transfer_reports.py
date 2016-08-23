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

from .auth import admin_required
from ..core import matching_data_source
from ..forms import ConfirmDeleteForm, TransferReportForm
from ..models import db_session, DataSource, Destination, TransferReport


routes = Blueprint("transfer_reports", __name__)


@routes.route("/transfer_reports", methods=["POST"])
def report_transfer():
    """
    Report a transfer.
    """
    form = TransferReportForm(request.form)
    form.destination.choices = [("", "Unknown")] + [(d.label, d.label) for d in Destination.query.all()]

    error_message = None
    if form.validate():
        data_source = matching_data_source(form.url.data)
        destination_id = None
        if form.destination.data:
            destination = Destination.query.filter(Destination.label == form.destination.data).first()
            if destination:
                destination_id = destination.id
        if data_source:
            report = TransferReport(
                data_source_id=data_source.id,
                report_id=max([r.report_id for r in data_source.transfer_reports] + [0]) + 1,
                destination_id=destination_id,
                url=form.url.data,
                file_size_bytes=form.file_size_bytes.data,
                transfer_duration_seconds=form.transfer_duration_seconds.data,
                file_checksum=form.file_checksum.data
            )

            try:
                db_session.add(report)
                db_session.commit()
            except:
                db_session.rollback()
                traceback.print_exc()
                error_message = "Failed to save report"
        else:
            error_message = "No data sources matches URL"
    else:
        error_message = "Invalid report"

    if error_message:
        return jsonify(success=False, error={"message": error_message})
    else:
        return jsonify(success=True, error=None)


@routes.route("/data_sources/<source_id>/transfer_reports")
@login_required
def list_transfer_reports(source_id):
    """
    Show reports of transfers from a data source.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first() or abort(404)

    page_num = int(request.args.get("page", 1))
    num_reports_per_page = 25
    reports = TransferReport.query.filter(TransferReport.data_source_id == source_id) \
        .order_by(TransferReport.created_at.desc()) \
        .limit(num_reports_per_page).offset((page_num - 1) * num_reports_per_page).all()
    total_num_reports = TransferReport.query.filter(TransferReport.data_source_id == source_id).count()
    total_num_pages = math.ceil(total_num_reports / num_reports_per_page)
    page_range = range(max(1, page_num - 3), min(total_num_pages, page_num + 3) + 1)
    return render_template("transfer_reports/index.html.jinja", data_source=data_source, reports=reports,
                           page_num=page_num, page_range=page_range, total_num_pages=total_num_pages)


@routes.route("/data_sources/<source_id>/transfer_reports/graph")
@login_required
def transfer_reports_graph(source_id):
    reports = TransferReport.query.filter((TransferReport.data_source_id == source_id) & (TransferReport.is_success == True)).all()  # noqa
    graph_data = [[r.created_at.timestamp(), r.transfer_rate] for r in reports]
    return jsonify(points=graph_data)


@routes.route("/data_sources/<source_id>/transfer_reports/<report_id>")
@login_required
def show_transfer_report(source_id, report_id):
    """
    Show information about a specific transfer report.
    """
    report = TransferReport.query.filter((TransferReport.data_source_id == source_id) & (TransferReport.report_id == report_id)).first() or abort(404)

    return render_template("transfer_reports/show.html.jinja", data_source=report.data_source, report=report)


@routes.route("/data_sources/<source_id>/transfer_reports/<report_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_transfer_report(source_id, report_id):
    """
    Delete a transfer report. Prompt for confirmation first.
    """
    form = ConfirmDeleteForm(request.form)
    report = TransferReport.query.filter((TransferReport.data_source_id == source_id) & (TransferReport.report_id == report_id)).first() or abort(404)

    if request.method == "POST" and form.validate():
        try:
            db_session.delete(report)
            db_session.commit()
            flash("Transfer report deleted", "success")
            return redirect(url_for("transfer_reports.list_transfer_reports", source_id=report.data_source_id))
        except:
            db_session.rollback()
            flash("Failed to delete transfer report", "danger")
            traceback.print_exc()

    return render_template("transfer_reports/delete.html.jinja", form=form, report=report)
