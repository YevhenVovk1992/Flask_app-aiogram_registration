from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    """
    Form for login user
    """
    name = StringField(
        label='Username',
        validators=[validators.length(max=25)],
        render_kw={"placeholder": "Username", "class": "input is-large"}
    )
    password = StringField(
        'Password',
        render_kw={"placeholder": "Password", "class": "input is-large"},
        widget=PasswordInput(hide_value=False)
    )
