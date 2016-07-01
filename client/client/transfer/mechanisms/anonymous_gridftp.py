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

from urllib.parse import urlsplit, urlunsplit

from .base import SimpleSubprocessMechanism


class AnonymousGridFTPMechanism(SimpleSubprocessMechanism):

    @classmethod
    def allowed_options(cls):
        return ("port", "username")

    @classmethod
    def transfer_program(cls):
        return "globus-url-copy"

    def transfer_command(self, url, output_path):
        parts = urlsplit(url)
        url = urlunsplit(("ftp", self.username + "@" + parts[1] + ":" + str(self.port), parts[2], parts[3], parts[4]))
        return ["globus-url-copy", url, "file://" + output_path]
