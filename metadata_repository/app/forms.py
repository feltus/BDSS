import wtforms

from .models import db_session, User
from .util import available_matcher_types, label_for_matcher_type
from .util import available_transfer_mechanism_types, label_for_transfer_mechanism_type
from .util import available_transform_types, label_for_transform_type


class Unique(object):
    """
    Custom validator to enforce unique user emails in database.
    """

    def __init__(self, model, field, scope={}, message=None):
        self.model = model
        self.field = field
        self.scope = scope

        if not message:
            message = "%s already taken" % field.lower().capitalize()
        self.message = message

    def __call__(self, form, field):
        self.scope[self.field] = field.data
        if db_session.query(self.model).filter_by(**self.scope).first():
            raise wtforms.validators.ValidationError(self.message)


class LoginForm(wtforms.Form):

    email = wtforms.fields.StringField(
        label="Email Address",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Email()])

    password = wtforms.fields.PasswordField(
        label="Password",
        validators=[wtforms.validators.InputRequired()])


class RegistrationForm(wtforms.Form):

    name = wtforms.fields.StringField(
        label="Name",
        validators=[wtforms.validators.InputRequired()])

    email = wtforms.fields.StringField(
        label="Email Address",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Email(), Unique(User, "email")])

    password = wtforms.fields.PasswordField(
        label="Password",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.Length(min=6)])

    password_confirmation = wtforms.fields.PasswordField(
        label="Confirm Password",
        validators=[wtforms.validators.InputRequired(), wtforms.validators.EqualTo("password", message="Passwords do not match")])


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


class UrlForm(wtforms.Form):
    """
    Form for entering URLs to check matches with data source(s) or to get transformed URLs.
    """

    url = wtforms.fields.StringField(
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


class TransferTestFileForm(wtforms.Form):
    """
    Form for adding test files to a data source.
    """

    url = wtforms.StringField(
        label="URL",
        validators=[wtforms.validators.InputRequired()])
