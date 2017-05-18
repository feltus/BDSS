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


cli_help = "Search data sources in metadata repository by label."


def configure_parser(parser):
    parser.add_argument("query",
                        help="Search for data sources matching this label")


def get_matching_data_sources(query):
    response = requests.get(metadata_repository_url + "/data_sources/search",
                            headers={"accept": "application/json"},
                            params={"q": query})
    return response.json()["data_sources"]


def handle_action(args, parser):
    data_sources = get_matching_data_sources(args.query)
    for source in data_sources:
        print((source["id"], source["label"]))
