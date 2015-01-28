# -*- coding: utf-8 -*-

from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError

from app import db
from app.models import User

from .base import CustomForm


class LoginForm(CustomForm):
    username = StringField('login', validators=[DataRequired()], description={'placeholder': "Username"})
    password = PasswordField('password', validators=[DataRequired()], description={'placeholder': "Password"})
    submit = SubmitField('submit')

    def validate_username(self, field):
        user = db.session.query(User).filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError('Invalid username or password')
        if not user.check_password(self.password.data):
            raise ValidationError('Invalid username or password')
