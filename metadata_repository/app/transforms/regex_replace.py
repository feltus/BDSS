import re

from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired

label = "Regex Search and Replace"


def transform_url(options, url):
    return re.sub(options["pattern"], options["repl"], url)


class OptionsForm(Form):

    pattern = StringField(label="Search Pattern",
                          validators=[InputRequired()])

    repl = StringField(label="Replacement",
                       validators=[InputRequired()])
