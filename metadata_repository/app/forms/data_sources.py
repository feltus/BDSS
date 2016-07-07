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

from .base import CSRFProtectedForm
from .fields import SelectWithOptionDescriptionField
from .validators import Unique
from ..models import DataSource
from ..util import available_transfer_mechanism_types, description_for_transfer_mechanism_type, label_for_transfer_mechanism_type


class DataSourceForm(CSRFProtectedForm):
    """
    Form for creating/editing a data source.
    """

    label = wtforms.fields.StringField(
        label="Label",
        validators=[wtforms.validators.InputRequired(), Unique(DataSource, "label")])

    description = wtforms.fields.TextAreaField(
        label="Description",
        validators=[wtforms.validators.Optional()])

    transfer_mechanism_type = SelectWithOptionDescriptionField(
        label="Transfer Mechanism",
        choices=[(t, label_for_transfer_mechanism_type(t)) for t in available_transfer_mechanism_types()],
        option_descriptions=[description_for_transfer_mechanism_type(t) for t in available_transfer_mechanism_types()],
        validators=[wtforms.validators.InputRequired()])

    transfer_mechanism_options = None


class DataSourceSearchForm(wtforms.Form):

    q = wtforms.fields.StringField(
        label="Query",
        validators=[wtforms.validators.DataRequired()])
