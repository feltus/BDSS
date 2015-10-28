import re

import wtforms

label = "Regular Expression"

def matches_url(options, url):
    if re.match(options["pattern"], url):
        return True
    else:
        return False

class OptionsForm(wtforms.Form):

    pattern = wtforms.fields.StringField(
        label="Pattern",
        validators=[wtforms.validators.InputRequired()],
        description="URLs will be matched against this pattern.")
