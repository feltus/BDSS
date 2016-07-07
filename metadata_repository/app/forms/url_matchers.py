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
from ..util import available_matcher_types, description_for_matcher_type, label_for_matcher_type


class UrlMatcherForm(CSRFProtectedForm):
    """
    Form for creating/editing a URL matcher.
    More fields will be contained in the options forms for the various matcher types.
    """

    matcher_type = SelectWithOptionDescriptionField(
        label="Matcher Type",
        choices=[(t, label_for_matcher_type(t)) for t in available_matcher_types()],
        option_descriptions=[description_for_matcher_type(t) for t in available_matcher_types()],
        validators=[wtforms.validators.InputRequired()])

    matcher_options = None
