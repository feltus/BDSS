import re

from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired

label = "Regular Expression"


def matches_url(options, url):
    if re.match(options["pattern"], url):
        return True
    else:
        return False


class OptionsForm(Form):

    pattern = StringField(label="Pattern",
                          validators=[InputRequired()],
                          description="URLs will be matched against this pattern.")
