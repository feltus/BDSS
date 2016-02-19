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

TransformResult = namedtuple("TransformResult", "original_url original_source transform_applied transformed_url")


class UrlTransformException(Exception):
    pass


def matching_data_source(url):
    """
    Find the data source that matches a URL.
    """
    matchers = UrlMatcher.query.all()
    if not matchers:
        raise UrlTransformException("No URL matchers configured")

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


def transform_url(url, available_mechanisms):
    """
    Query DB for alternate URLs for the data file at the given URL.
    """
    transform_results = []
    data_source = matching_data_source(url)

    if not data_source:
        raise UrlTransformException("No data source matches URL")

    # For all matching data sources, apply all transforms
    for transform in data_source.transforms:
        transformed_url = transform.transform_url(url)

        # If transformed URL matches target data source, add to results
        # Include matcher and transform in result for display
        if transform.to_data_source.matches_url(transformed_url) and \
           transform.to_data_source.transfer_mechanism_type in available_mechanisms:

            transform_results.append(TransformResult(
                original_url=url,
                original_source=data_source,
                transform_applied=transform,
                transformed_url=transformed_url
            ))

        else:
            # FIXME: This should be a log
            print("Transformed URL did not match target data source", file=sys.stderr)

    # TODO: If no matching sources have transforms, raise exception.

    return transform_results
