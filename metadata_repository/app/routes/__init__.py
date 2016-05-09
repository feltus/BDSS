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

# flake8: noqa

from .auth import routes as auth_routes
from .core import routes as core_routes
from .data_sources import routes as data_source_routes
from .matchers import routes as matcher_routes
from .test_files import routes as test_file_routes
from .timing_reports import routes as timing_report_routes
from .transforms import routes as transform_routes
from .users import routes as user_routes
