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

label = "Regex Search and Replace"


description = "Substitute with a regular expression"


def transform_url(options, url):
    return re.sub(options["pattern"], options["repl"], url)


class OptionsForm(Form):

    pattern = StringField(label="Search Pattern",
                          validators=[InputRequired()],
                          description="Pattern to replace")

    repl = StringField(label="Replacement",
                       validators=[InputRequired()],
                       description="Replace occurrences of 'Search Pattern' with this")


def render_description(options):
    return "Replace regular expression \'" + options["pattern"] + "\' with \'" + options["repl"] + "\'"
