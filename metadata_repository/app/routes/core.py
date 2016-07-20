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

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from ..core import find_transfers, FindTransferError
from ..forms import FindTransfersForm
from ..models import Destination


routes = Blueprint("core", __name__)


######################################################################################################
#
# Misc routes
#
######################################################################################################


@routes.route("/")
def index():
    """Home page"""
    return redirect(url_for("data_sources.list_data_sources"))


@routes.route("/transfers", methods=["GET", "POST"])
def transfers():
    """
    Find available transfers for a URL.
    """
    form = FindTransfersForm(request.form)
    form.destination.choices = [("", "Unknown")] + [(d.label, d.label) for d in Destination.query.all()]

    results = []
    if request.method == "POST":
        error_message = None
        if form.validate():
            try:
                destination = None
                if form.destination.data:
                    destination = Destination.query.filter(Destination.label == form.destination.data).first()
                results = find_transfers(form.url.data, form.available_mechanisms.data, destination)
            except FindTransferError as e:
                error_message = e.args[0]
            except Exception as e:
                traceback.print_exc()
                error_message = "Unable to find transfers"
        else:
            error_message = "Validation error"

        if request.headers.get("Accept") == "application/json":
            return jsonify(transfers=results, error={"message": error_message})
        elif error_message:
            flash(error_message, "danger")

    return render_template("transfers.html.jinja", form=form, transfers=results)
