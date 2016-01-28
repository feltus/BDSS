import wtforms


label = "Aspera"


class OptionsForm(wtforms.Form):

    username = wtforms.fields.StringField(
        label="Username",
        validators=[wtforms.validators.InputRequired()])

    disable_encryption = wtforms.fields.BooleanField(
        label="Disable Encryption",
        validators=[wtforms.validators.InputRequired()])
