# -*- coding: utf-8 -*-

from slugify import slugify

from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from .base import CustomForm

from app import db
from app.models import User


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

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=self.username.data).first() is not None:
            raise ValidationError("This username is already taken")
        if db.session.query(User).filter_by(blog_slug=slugify(self.username.data)).first() is not None:
            raise ValidationError("This username is already taken")
