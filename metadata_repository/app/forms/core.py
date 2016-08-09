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

import wtforms

from ..util import available_transfer_mechanism_types, label_for_transfer_mechanism_type


class FindTransfersForm(wtforms.Form):

    available_mechanisms = wtforms.fields.SelectMultipleField(
        label="Available Mechanisms",
        choices=[(mech, label_for_transfer_mechanism_type(mech)) for mech in available_transfer_mechanism_types()],
        validators=[wtforms.validators.InputRequired()])

    destination = wtforms.fields.SelectField(
        label="Destination",
        validators=[wtforms.validators.Optional()])

    url = wtforms.fields.StringField(
        label="URL",
        validators=[wtforms.validators.InputRequired()])
