import wtforms

from .util import available_matcher_types, label_for_matcher_type

class DataSourceForm(wtforms.Form):
    """
    Form for creating/editing a data source.
    """

    label = wtforms.fields.StringField(
        label="Label",
        validators=[wtforms.validators.InputRequired()])

class UrlMatcherForm(wtforms.Form):
    """
    Form for creating/editing a URL matcher.
    More fields will be contained in the options forms for the various matcher types.
    """

    matcher_type = wtforms.fields.SelectField(
        label="Matcher Type",
        choices=[(t, label_for_matcher_type(t)) for t in available_matcher_types()],
        validators=[wtforms.validators.InputRequired()])

    matcher_options = None

class TestMatchForm(wtforms.Form):
    """
    Form for testing whether or not a URL matches data source(s).
    """

    test_url = wtforms.fields.StringField(
        label="URL to test",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.URL(require_tld=False)])
