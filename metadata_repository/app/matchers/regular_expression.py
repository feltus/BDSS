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

from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired

label = "Regular Expression"


description = "Match based on a regular expression"


def matches_url(options, url):
    if re.match(options["pattern"], url):
        return True
    else:
        return False


class OptionsForm(Form):

    pattern = StringField(label="Pattern",
                          validators=[InputRequired()],
                          description="URLs will be matched against this pattern.")


def render_description(options):
    return "Match regular expression \'" + options["pattern"] + "\'"
