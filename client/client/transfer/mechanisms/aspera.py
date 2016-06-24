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

import os
from urllib.parse import urlparse, urlunsplit

from .base import SimpleSubprocessMechanism


class AsperaMechanism(SimpleSubprocessMechanism):

    @classmethod
    def allowed_options(cls):
        return ("disable_encryption", "username")

    @classmethod
    def transfer_program(cls):
        return "ascp"

    def _transfer_command(self, url, output_path):

        default_path_to_key = os.path.expandvars(os.path.join("$HOME", ".aspera", "connect", "etc", "asperaweb_id_dsa.openssh"))
        args = ["-i", default_path_to_key]

        # Require encryption?
        try:
            if self.disable_encryption:
                args.append("-T")
        except KeyError:
            pass

        # Remove scheme from URL
        parts = urlparse(url)
        url = parts[1] + ":" + urlunsplit(("", "", parts[2], parts[3], parts[4]))

        return ["ascp"] + args + [self.username + "@" + url, output_path]
