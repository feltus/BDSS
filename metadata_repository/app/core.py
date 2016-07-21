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

import sys
from collections import namedtuple

from .models import UrlMatcher

Transfer = namedtuple("Transfer", ["url", "mechanism_name", "mechanism_options", "data_source_id"])


class FindTransferError(Exception):
    pass


def matching_data_source(url):
    """
    Find the data source that matches a URL.
    """
    matchers = UrlMatcher.query.all()
    if not matchers:
        raise FindTransferError("No URL matchers configured")

    # Check URL against all matchers
    # Skip matchers for data sources that have already checked
    checked_sources = set()
    matching_sources = []
    for m in matchers:
        if m.data_source_id not in checked_sources and m.matches_url(url):
            checked_sources.add(m.data_source_id)
            matching_sources.append(m.data_source)

    if len(matching_sources) > 1:
        # FIXME: This should be a log
        print("Warning: Multiple data sources match URL '%s'. Likely matcher misconfiguration.", file=sys.stderr)

    if matching_sources:
        return matching_sources[0]
    else:
        return None


def find_transfers(url, available_mechanisms, destination=None):
    """
    Query DB for alternate URLs for the data file at the given URL.
    """
    transfers = []
    data_source = matching_data_source(url)

    if not data_source:
        raise FindTransferError("No data source matches URL")

    # For all matching data sources, apply all transforms
    for transform in data_source.transforms:

        if transform.for_destinations:
            if not destination or destination not in transform.for_destinations:
                continue

        transformed_url = transform.transform_url(url)

        # If transformed URL matches target data source, add to results
        # Include matcher and transform in result for display
        if transform.to_data_source.matches_url(transformed_url) and \
           transform.to_data_source.transfer_mechanism_type in available_mechanisms:

            transfer = Transfer(
                url=transformed_url,
                mechanism_name=transform.to_data_source.transfer_mechanism_type,
                mechanism_options=transform.to_data_source.transfer_mechanism_options,
                data_source_id=transform.to_data_source.id)

            transfers.append(transfer)

        else:
            # FIXME: This should be a log
            print("Transformed URL did not match target data source", file=sys.stderr)

    # Add a transfer from the original data source
    original_transfer = Transfer(
        url=url,
        mechanism_name=data_source.transfer_mechanism_type,
        mechanism_options=data_source.transfer_mechanism_options,
        data_source_id=data_source.id)

    transfers.append(original_transfer)

    return transfers
