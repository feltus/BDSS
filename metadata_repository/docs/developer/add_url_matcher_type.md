# Add URL Matcher Type

This explains how to add support for a new type of URL matcher to the metadata repository.

Each URL matcher type corresponds to a module in `app/matchers` that conforms to a specific
API. To generate stub code for a new matcher type, run `./scripts/gen/url_matcher id` from
the BDSS project root, replacing `id` with the ID of the new matcher type. This will create
a file at `metadata_repository/app/matchers/id.py` with stubs for the required functions.

## URL Matcher API

Each URL matcher module must have the following functions defined:

```Python
label = "Matcher Name"
"""
A human readable name for the matcher type. This will be displayed in the list of
available matcher types when adding or editing a matcher.
"""


description = "Matches based on something"
"""
Human readable description of how the matcher operates. This will be displayed
when the user selects this type when adding or editing a matcher.
"""


def matches_url(options, url):
    """
    Check if a URL matches or not. Returns True or False.

    Arguments:
    options - dict - Matcher options from the OptionsForm below. Keys match field
                     names in the form and values are form input values.
    url - str - The URL to check.
    """
    return False


class OptionsForm(wtforms.Form):
    """
    Matcher options form displayed when adding/editing a matcher.
    Must be a subclass of wtforms.Form.
    """
    pass


def render_description(options):
    """
    Returns a human readable string that will be displayed in the list of matchers
    on a data source's information page.
    """
    return "Match URLs somehow"
```
