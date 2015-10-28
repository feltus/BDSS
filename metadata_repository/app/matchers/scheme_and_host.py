from urllib.parse import urlparse

import wtforms

label = "Scheme and Host"

def matches_url(options, url):
    parsed = urlparse(url)
    if parsed.scheme == options["scheme"] and parsed.hostname == options.host:
        return True
    else:
        return False

# List of URL schemes supported by urlparse
# https://docs.python.org/3/library/urllib.parse.html
_supported_schemes = ["file", "ftp", "gopher", "hdl", "http", "https", "imap",
    "mailto", "mms", "news", "nntp", "prospero", "rsync", "rtsp", "rtspu", "sftp",
    "shttp", "sip", "sips", "snews", "svn", "svn+ssh", "telnet", "wais"]

class OptionsForm(wtforms.Form):

    scheme = wtforms.fields.SelectField(
        label="Scheme",
        choices=[(s, s) for s in _supported_schemes],
        validators=[wtforms.validators.InputRequired()])

    host = wtforms.fields.StringField(
        label="Host",
        validators=[wtforms.validators.InputRequired()])
