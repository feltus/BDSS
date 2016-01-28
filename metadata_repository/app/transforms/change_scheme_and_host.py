from urllib.parse import urlparse, urlunsplit

import wtforms

label = "Change Scheme and Host"


def transform_url(options, url):
    parts = urlparse(url)
    return urlunsplit((options["new_scheme"], options["new_host"], parts.path, parts.query, parts.fragment))


class OptionsForm(wtforms.Form):

    new_scheme = wtforms.fields.StringField(label="New scheme",
                                            validators=[wtforms.validators.InputRequired()])

    new_host = wtforms.fields.StringField(label="New host",
                                          validators=[wtforms.validators.InputRequired()])


def render_description(options):
    return "Change URL scheme to \'" + options["new_scheme"] + "\' and host to \'" + options["new_host"] + "\'"
