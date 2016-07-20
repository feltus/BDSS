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

import re

import wtforms


class TransferReportForm(wtforms.Form):
    """
    Form for reporting transfer times.
    """

    is_success = wtforms.BooleanField(
        false_values=('false', 'False', ''),
        label="Successful Transfer")

    url = wtforms.StringField(
        label="URL",
        validators=[wtforms.validators.InputRequired()])

    destination = wtforms.fields.SelectField(
        label="Destination",
        validators=[wtforms.validators.Optional()])

    file_size_bytes = wtforms.IntegerField(
        label="File Size (bytes)",
        validators=[wtforms.validators.InputRequired()])

    transfer_duration_seconds = wtforms.FloatField(
        label="Transfer Duration (seconds)",
        validators=[wtforms.validators.InputRequired()])

    file_checksum = wtforms.StringField(
        label="MD5 Checksum")

    def validate_file_checksum(form, field):
        if form.file_size_bytes.data > 0:
            if not field.data:
                raise wtforms.ValidationError("This field is required")
            if not re.match(r"[0-9A-Fa-f]{32}", field.data):
                raise wtforms.ValidationError("Invalid checksum")

    mechanism_output = wtforms.fields.TextAreaField(
        label="Mechanism Output",
        validators=[wtforms.validators.Optional()])
