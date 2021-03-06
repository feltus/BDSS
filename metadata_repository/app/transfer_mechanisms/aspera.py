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


label = "Aspera"


description = "Transfer files with Aspera Connect's <a href=\"http://download.asperasoft.com/download/docs/ascp/3.5.2/html/index.html/\">ascp</a>"


class OptionsForm(wtforms.Form):

    username = wtforms.fields.StringField(
        label="Username",
        validators=[wtforms.validators.InputRequired()])

    disable_encryption = wtforms.fields.BooleanField(
        label="Disable Encryption")
