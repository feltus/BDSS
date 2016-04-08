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

from urllib.parse import urlparse

from . import aspera
from . import curl
from . import gridftp_lite
from . import scp


all_mechanisms = {
    "aspera": aspera,
    "curl": curl,
    "gridftp_lite": gridftp_lite,
    "scp": scp
}


def available_mechanisms():
    """
    Names of all available transfer mechanisms.
    """
    return [name for name, module in all_mechanisms.items() if module.is_available()]


def default_mechanism(url):
    """
    Name of the default transfer mechanism for a URL.
    This is used if the metadata repository doesn't specify a mechanism.

    Returns
    Tuple of mechanism name and options.
    """
    method_for_scheme = {
        "aspera": "aspera",
        "sshftp": "gridftp_lite",
        "scp": "scp"
    }
    return (method_for_scheme.get(urlparse(url).scheme, "curl"), None)
