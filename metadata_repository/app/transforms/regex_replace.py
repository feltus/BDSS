import re

import wtforms

label = "Regex Search and Replace"

def transform_url(options, url):
    return re.sub(options["pattern"], options["repl"], url)

class OptionsForm(wtforms.Form):

    pattern = wtforms.fields.StringField(
        label="Search Pattern",
        validators=[wtforms.validators.InputRequired()])

    repl = wtforms.fields.StringField(
        label="Replacement",
        validators=[wtforms.validators.InputRequired()])
