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
from .validators import Unique
from ..models import User


class LoginForm(CSRFProtectedForm):

    email = wtforms.fields.StringField(
        label="Email Address",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Email()])

    password = wtforms.fields.PasswordField(
        label="Password",
        validators=[wtforms.validators.InputRequired()])


class RegistrationForm(CSRFProtectedForm):

    name = wtforms.fields.StringField(
        label="Name",
        validators=[wtforms.validators.InputRequired()])

    email = wtforms.fields.StringField(
        label="Email Address",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Email(), Unique(User, "email")])

    password = wtforms.fields.PasswordField(
        label="Password",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Length(min=6)])

    password_confirmation = wtforms.fields.PasswordField(
        label="Confirm Password",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.EqualTo("password", message="Passwords do not match")])
