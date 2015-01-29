# -*- coding: utf-8 -*-

from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from .base import CustomForm


class PostForm(CustomForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)])
    content = TextAreaField('Post', validators=[DataRequired()])

