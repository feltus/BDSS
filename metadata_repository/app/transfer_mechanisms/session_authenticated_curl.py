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


label = "curl with authenticated session"


description = "Transfer files with curl using a session created by authenticating at a separate endpoint"


class OptionsForm(wtforms.Form):

    auth_url = wtforms.fields.StringField(
        label="The URL to authenticate to",
        validators=[wtforms.validators.InputRequired()])

    username_field = wtforms.fields.StringField(
        label="The name of the username field at the authentication URL",
        validators=[wtforms.validators.InputRequired()])

    password_field = wtforms.fields.StringField(
        label="The name of the password field at the authentication URL",
        validators=[wtforms.validators.InputRequired()])

    username_prompt = wtforms.fields.StringField(
        label="Prompt shown to user when requesting username",
        validators=[wtforms.validators.InputRequired()])

    password_prompt = wtforms.fields.StringField(
        label="Prompt shown to user when requesting password",
        validators=[wtforms.validators.InputRequired()])
