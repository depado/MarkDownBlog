# -*- coding: utf-8 -*-

from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo

from .base import CustomForm

class RegisterForm(CustomForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=25)],
        description={'placeholder': "Username"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4), EqualTo('confirm', message='Passwords must match')],
        description={'placeholder': "Password"}
    )
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired()],
        description={'placeholder': "Repeat Password"}
    )
