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

import tempfile

from .base import BaseMechanism, UserInputOption
from ...util import is_program_on_path, run_subprocess


class SessionAuthenticatedCurlMechanism(BaseMechanism):

    @classmethod
    def allowed_options(self):
        return [
            # Curator provided
            "auth_url",
            "username_field",
            "password_field",
            "username_prompt",
            "password_prompt",
            # User provided
            "username",
            "password"
        ]

    @classmethod
    def is_available(cls):
        return is_program_on_path("curl")

    def user_input_options(self):
        return [
            UserInputOption("username", self.username_prompt),
            UserInputOption("password", self.password_prompt)
        ]

    def transfer_file(self, url, output_path):
        with tempfile.NamedTemporaryFile(delete=True) as cookie_jar:
            (success, output1) = run_subprocess([
                "curl",
                "--cookie-jar", cookie_jar.name,
                "--data-urlencode", "%s=%s" % (self.username_field, self.username),
                "--data-urlencode", "%s=%s" % (self.password_field, self.password),
                self.auth_url
            ])

            if not success:
                return (success, output1)
            else:
                (success, output2) = run_subprocess([
                    "curl",
                    "--cookie", cookie_jar.name,
                    "--output", output_path,
                    url
                ])

                return (success, output1 + "\n" + output2)
