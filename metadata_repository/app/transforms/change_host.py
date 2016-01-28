from urllib.parse import urlparse, urlunsplit

import wtforms

label = "Change Host"


def transform_url(options, url):
    parts = urlparse(url)
    return urlunsplit((parts.scheme, options["new_host"], parts.path, parts.query, parts.fragment))


class OptionsForm(wtforms.Form):

    new_host = wtforms.fields.StringField(label="New Host",
                                          validators=[wtforms.validators.InputRequired()])
