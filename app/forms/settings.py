# -*- coding: utf-8 -*-

from wtforms.fields import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional

from .base import CustomForm
from .utils import ImageUrl


class SettingForm(CustomForm):
    blog_title = StringField(
        'Blog Title',
        validators=[DataRequired(), Length(min=5, max=50)],
        description={'placeholder': "Blog Title"}
    )
    blog_description = TextAreaField(
        'Blog Description',
        validators=[DataRequired(), Length(min=5, max=200)],
        description={'placeholder': "Blog Description"}
    )
    blog_image = StringField(
        'Blog Image',
        validators=[Optional(), URL(), ImageUrl()],
        description={'placeholder': "Blog Image"}
    )
    blog_image_rounded = BooleanField(
        'Round Blog Image',
    )
    blog_bg = StringField(
        'Blog Background',
        validators=[Optional(), URL(), ImageUrl()],
        description={'placeholder': "Blog Background"}
    )
    blog_bg_public = BooleanField(
        'Blog Background Public'
    )
    blog_bg_repeat = BooleanField(
        'Blog Background Repeat'
    )
    blog_bg_everywhere = BooleanField(
        'Blog Background Everywhere'
    )
    blog_bg_override = BooleanField(
        'Blog Background Override'
    )


