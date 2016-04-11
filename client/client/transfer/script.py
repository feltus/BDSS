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

import json
import os
from pkg_resources import resource_string


def _format(url_to_transfer):
    return {
        "u": url_to_transfer["url"],
        "o": url_to_transfer["output_file_name"],
        "c": [spec.transfer_command(os.path.join(".", url_to_transfer["output_file_name"])) for spec in url_to_transfer["transfer_specs"]]
    }


def generate_script(urls_to_transfer):
    template = resource_string(__name__, "script_template.py").decode("utf-8")
    urls_for_template = [_format(u) for u in urls_to_transfer]
    return template.format(urls=json.dumps(urls_for_template, indent=2, sort_keys=True))
