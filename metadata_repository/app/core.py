from collections import namedtuple
import sys

from .models import DataSource, UrlMatcher, Transform

TransformResult = namedtuple("TransformResult", "original_url original_source transform_applied transformed_url")

def transform_url(url):

    matchers = UrlMatcher.query.all()

    # If no data sources/matchers, flash error
    if not matchers:
        raise Exception("No URL matchers configured")

    transform_results = []

    processed_sources = set()
    for m in matchers:

        # Check URL against all matchers
        # Skip matchers for data sources that have already matched
        if m.data_source_id in processed_sources or not m.matches_url(url):
            continue

        # For all matching data sources, apply all transforms
        for t in m.data_source.transforms:
            transformed_url = t.transform_url(url)

            # If transformed URL matches target data source, add to results
            # Include matcher and transform in result for display
            if t.to_data_source.matches_url(transformed_url):
                transform_results.append(TransformResult(
                    original_url=url,
                    original_source=m.data_source,
                    transform_applied=t,
                    transformed_url=transformed_url
                ))

            else:
                print("Transformed URL did not match target data source", file=sys.stderr)

        # TODO: If no matching sources have transforms, flash error

    return transform_results
