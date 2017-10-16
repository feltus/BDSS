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

import json

import requests
import sqlalchemy as sa
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required

from .auth import admin_required
from ..models import db_session, DataSource, Destination, TransferTestFile, Transform, UrlMatcher


routes = Blueprint("configuration", __name__)


# Serialize configuration for export

def serialize_matcher(matcher):
    return dict(type=matcher.matcher_type, options=matcher.matcher_options)


def serialize_transform(transform):
    return dict(
        target=transform.to_data_source.label,
        for_destinations=[d.label for d in transform.for_destinations],
        type=transform.transform_type,
        options=transform.transform_options
    )


def serialize_data_source(source):
    return dict(
        label=source.label,
        description=source.description,
        transfer_mechanism=dict(
            type=source.transfer_mechanism_type,
            options=source.transfer_mechanism_options),
        test_files=[f.url for f in source.transfer_test_files],
        transforms=[serialize_transform(t) for t in source.transforms],
        url_matchers=[serialize_matcher(m) for m in source.url_matchers]
    )


def serialize_destination(dest):
    return dict(label=dest.label, description=dest.description)


def serialize_configuration():
    serialized_data_sources = [serialize_data_source(s) for s in DataSource.query.all()]
    serialized_destinations = [serialize_destination(d) for d in Destination.query.all()]

    return dict(data_sources=serialized_data_sources,
                destinations=serialized_destinations)


# Populate database from serialized configuration


class LoadConfigurationError(Exception):
    pass


def load_configuration(conf):
    try:
        conf = json.loads(conf)
    except json.decoder.JSONDecodeError:
        raise LoadConfigurationError("Invalid configuration file")
    else:
        destinations_conf = conf["destinations"]
        destinations = {d["label"]: Destination(**d) for d in destinations_conf}
        for label, dest in destinations.items():
            db_session.add(dest)

        sources_conf = conf["data_sources"]
        sources = {}
        for s in sources_conf:
            source = DataSource(
                label=s["label"],
                description=s["description"],
                transfer_mechanism_type=s["transfer_mechanism"]["type"],
                transfer_mechanism_options=s["transfer_mechanism"]["options"]
            )

            for i, url in enumerate(s["test_files"]):
                source.transfer_test_files.append(TransferTestFile(file_id=i+1, url=url))

            for i, m in enumerate(s["url_matchers"]):
                source.url_matchers.append(UrlMatcher(
                    matcher_id=i+1,
                    matcher_type=m["type"],
                    matcher_options=m["options"]
                ))

            sources[source.label] = source

        for s in sources_conf:
            source = sources[s["label"]]
            for i, t in enumerate(s["transforms"]):
                transform = Transform(
                    transform_id=i+1,
                    preference_order=i,
                    to_data_source=sources[t["target"]],
                    for_destinations=[destinations[dest] for dest in t["for_destinations"]],
                    transform_type=t["type"],
                    transform_options=t["options"]
                )
                source.transforms.append(transform)

        for label, source in sources.items():
            db_session.add(source)

        try:
            db_session.commit()
        except sa.exc.IntegrityError as e:
            db_session.rollback()
            raise LoadConfigurationError("Unable to overwrite existing configuration") from e
        except Exception as e:
            db_session.rollback()
            raise LoadConfigurationError("Failed to save configuration") from e


# Route handlers


@routes.route("/configuration")
def index():
    return render_template("configuration/index.html.jinja")


@routes.route("/configuration/export")
def export_configuration():
    """Export configuration of data sources, matchers, destinations, and transforms to a file."""
    return jsonify(**serialize_configuration())


@routes.route("/configuration/import", methods=("GET", "POST"))
@login_required
@admin_required
def import_configuration():
    """Export configuration of data sources, matchers, destinations, and transforms from an uploaded file."""

    upload_error = None
    url_error = None
    status = 200
    if request.method == "POST":
        import_url = request.form.get("from_url", None)
        uploaded_file = request.files.get("conf_file", None)

        if "conf_file" in request.files and uploaded_file:
            uploaded_conf = uploaded_file.read().decode("utf-8")
            uploaded_file.close()
            try:
                load_configuration(uploaded_conf)
            except LoadConfigurationError as e:
                upload_error = str(e)
            except Exception as e:
                upload_error = "Unknown error"
        elif "from_url" in request.form and import_url:
            try:
                response = requests.get(import_url, timeout=10)
                response.raise_for_status()
                load_configuration(response.text)
            except LoadConfigurationError as e:
                url_error = str(e)
            except requests.exceptions.RequestException:
                url_error = "Unable to load configuration from %s" % import_url
            except Exception as e:
                url_error = "Unknown error"
        else:
            upload_error = url_error = "Configuration file or URL is required"

        if upload_error or url_error:
            flash("Import failed", "danger")
            status = 400
        else:
            flash("Import successful", "success")

    return (render_template("configuration/import.html.jinja", upload_error=upload_error, url_error=url_error), status)
