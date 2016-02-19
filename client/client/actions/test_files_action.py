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

import requests

from ..config import metadata_repository_url


def configure_parser(parser):
    parser.add_argument("data_source_id",
                        help="ID of data source to get test files for",
                        metavar="data-source-id")


def get_test_files(data_source_id):
    """
    Retrieve test files for a data source from the metadata repository.

    Parameters:
    data_source_id - Integer - ID of data source to get test files for
    """
    response = requests.get("/".join([metadata_repository_url, "data_sources", data_source_id, "test_files"]), headers={
        "accept": "application/json"
    })
    return response.json()["test_files"]


def handle_action(args, parser):
    test_files = get_test_files(args.data_source_id)
    for f in test_files:
        print(f["url"])
