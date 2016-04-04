# Add URL Transform Type

This explains how to add support for a new type of URL transform to the metadata repository.

Each URL transform type corresponds to a module in `app/transforms` that conforms to a specific
API. To generate stub code for a new transform type, run `./scripts/gen/url_transform id` from
the BDSS project root, replacing `id` with the ID of the new transform type. This will create
a file at `metadata_repository/app/transforms/id.py` with stubs for the required functions.

## URL Transform API

Each URL transform module must have the following functions defined:

```Python
label = "Transform Name"
"""
A human readable name for the transform type. This will be displayed in the list of
available transform types when adding or editing a transform.
"""


description = "Transforms URL somehow"
"""
Human readable description of how the transform operates. This will be displayed
when the user selects this type when adding or editing a transform.
"""


def transform_url(options, url):
    """
    Transform a URL into another URL based on the given transform options. Returns
    the transformed URL.

    Arguments:
    options - dict - Transform options from the OptionsForm below. Keys match field
                     names in the form and values are form input values.
    url - str - The URL to transform.
    """
    return url


class OptionsForm(wtforms.Form):
    """
    Transform options form displayed when adding/editing a transform.
    Must be a subclass of wtforms.Form.
    """
    pass


def render_description(options):
    """
    Returns a human readable string that will be displayed in the list of transforms
    on a data source's information page.
    """
    return "Transforms URLs somehow"
```
