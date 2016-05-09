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

from ..core import transform_url, UrlTransformException
from ..forms import TransformedUrlsForm


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


@routes.route("/transformed_urls", methods=["GET", "POST"])
def get_transformed_urls():
    """
    Find transformed URLs for a URL.
    """
    form = TransformedUrlsForm(request.form)

    results = []
    if request.method == "POST":
        error_message = None
        if form.validate():
            try:
                results = transform_url(form.url.data, form.available_mechanisms.data)
            except UrlTransformException as e:
                error_message = e.args[0]
            except Exception as e:
                traceback.print_exc()
                error_message = "Unable to transform URL"
        else:
            error_message = "Validation error"

        if request.headers.get("Accept") == "application/json":
            return jsonify(results=results, error={"message": error_message})
        elif error_message:
            flash(error_message, "danger")

    return render_template("get_transformed_urls.html.jinja", form=form, results=results)
