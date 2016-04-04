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

label = "Change Hostname"


description = "Replace the hostname of the original URL"


def transform_url(options, url):
    parts = urlparse(url)
    return urlunsplit((parts.scheme, options["new_host"], parts.path, parts.query, parts.fragment))


class OptionsForm(wtforms.Form):

    new_host = wtforms.fields.StringField(label="New Hostname",
                                          validators=[wtforms.validators.InputRequired()],
                                          description="The new hostname for the transformed URL")


def render_description(options):
    return "Change URL hostname to \'" + options["new_host"] + "\'"
