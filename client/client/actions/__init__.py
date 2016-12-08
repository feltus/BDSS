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

from . import config_action
from . import mechanisms_action
from . import sources_action
from . import test_files_action
from . import transfer_action
from . import version_action


_actions = {
    "config": config_action,
    "mechanisms": mechanisms_action,
    "sources": sources_action,
    "test_files": test_files_action,
    "transfer": transfer_action,
    "version": version_action
}


def all_actions():
    return sorted(list(_actions.keys()))


def action_module(action_name):
    return _actions[action_name]


def available_action_info():
    return [(action, getattr(action_module(action), "cli_help", "")) for action in all_actions()]
