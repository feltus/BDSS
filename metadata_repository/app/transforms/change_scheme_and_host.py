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

from urllib.parse import urlparse, urlunsplit

import wtforms

label = "Change Scheme and Hostname"


description = "Replace the original URL's scheme and hostname"


def transform_url(options, url):
    parts = urlparse(url)
    return urlunsplit((options["new_scheme"], options["new_host"], parts.path, parts.query, parts.fragment))


class OptionsForm(wtforms.Form):

    new_scheme = wtforms.fields.StringField(label="New scheme",
                                            validators=[wtforms.validators.InputRequired()],
                                            description="The new scheme for the transformed URL")

    new_host = wtforms.fields.StringField(label="New hostname",
                                          validators=[wtforms.validators.InputRequired()],
                                          description="The new hostname for the transformed URL")


def render_description(options):
    return "Change URL scheme to \'" + options["new_scheme"] + "\' and hostname to \'" + options["new_host"] + "\'"
