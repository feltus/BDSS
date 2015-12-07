import wtforms

from .util import available_matcher_types, label_for_matcher_type
from .util import available_transfer_mechanism_types, label_for_transfer_mechanism_type
from .util import available_transform_types, label_for_transform_type


class DataSourceForm(wtforms.Form):
    """
    Form for creating/editing a data source.
    """

    label = wtforms.fields.StringField(
        label="Label",
        validators=[wtforms.validators.InputRequired()])

    transfer_mechanism_type = wtforms.fields.SelectField(
        label="Transfer Mechanism",
        choices=[(t, label_for_transfer_mechanism_type(t)) for t in available_transfer_mechanism_types()],
        validators=[wtforms.validators.InputRequired()])

    transfer_mechanism_options = None


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


class UrlTransformForm(wtforms.Form):
    """
    Form for creating/editing a URL transform between data sources.
    More fields will be contained in the options forms for the various transform types.
    """

    to_data_source_id = wtforms.fields.SelectField(
        label="Data source to transform to",
        choices=[],
        coerce=int,
        validators=[wtforms.validators.InputRequired()])

    transform_type = wtforms.fields.SelectField(
        label="Transform Type",
        choices=[(t, label_for_transform_type(t)) for t in available_transform_types()],
        validators=[wtforms.validators.InputRequired()])

    transform_options = None

    description = wtforms.fields.TextAreaField(
        label="Description",
        validators=[wtforms.validators.Optional()])


class TestUrlForm(wtforms.Form):
    """
    Form for testing whether or not a URL matches data source(s).
    """

    test_url = wtforms.fields.StringField(
        label="URL",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.URL(require_tld=False)])


class TimingReportForm(wtforms.Form):
    """
    Form for reporting transfer times.
    """

    url = wtforms.StringField(
        label="URL",
        validators=[wtforms.validators.InputRequired()])

    file_size_bytes = wtforms.IntegerField(
        label="File Size (bytes)",
        validators=[wtforms.validators.InputRequired()])

    transfer_duration_seconds = wtforms.FloatField(
        label="Transfer Duration (seconds)",
        validators=[wtforms.validators.InputRequired()])
