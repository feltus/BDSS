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


def transform_url(url):
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
        if transform.to_data_source.matches_url(transformed_url):
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
