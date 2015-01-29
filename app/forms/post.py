# -*- coding: utf-8 -*-

from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from .base import CustomForm


class PostForm(CustomForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)], description={'placeholder': "Title"})
    content = TextAreaField('Post', validators=[DataRequired()], description={'placeholder': "Content (MarkDown)"})

