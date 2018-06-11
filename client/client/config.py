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

import configparser
import os
from pkg_resources import resource_string


config = configparser.ConfigParser()
config.read_string(resource_string(__name__, "defaults.cfg").decode("utf-8"))
config.read(["/etc/bdss.cfg", os.path.expanduser("~/.bdss.cfg"), "bdss.cfg"])


CONFIGURABLE_OPTIONS = [
    "metadata_repository.url",
    "client.location",
    "dtn.host",
    "dtn.user",
    "dtn.path"
]


def get_config(key):
    if key not in CONFIGURABLE_OPTIONS:
        raise Exception("\"%s\" is not a configuration key" % key)

    [section, option] = key.split(".")

    return config.get(section, option, fallback=None)


def set_config(key, value):
    if key not in CONFIGURABLE_OPTIONS:
        raise Exception("\"%s\" is not a configuration key" % key)

    [section, option] = key.split(".")
    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, str(value))

    with open(os.path.expanduser("~/.bdss.cfg"), "w") as f:
        config.write(f)


def clear_config(key):
    if key not in CONFIGURABLE_OPTIONS:
        raise Exception("\"%s\" is not a configuration key" % key)

    [section, option] = key.split(".")
    if not config.has_section(section):
        config.add_section(section)

    config.remove_option(section, option)

    with open(os.path.expanduser("~/.bdss.cfg"), "w") as f:
        config.write(f)


metadata_repository_url = get_config("metadata_repository.url").rstrip("/")

client_destination = get_config("client.location")

dtn_host = get_config("dtn.host")
dtn_path = get_config("dtn.path")
dtn_user = get_config("dtn.user")
