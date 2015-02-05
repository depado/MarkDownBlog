# -*- coding: utf-8 -*-

import requests
import imghdr

from wtforms.fields import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional
from wtforms import ValidationError

from .base import CustomForm


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
        validators=[Optional(), URL()],
        description={'placeholder': "Blog Image"}
    )
    blog_round_image = BooleanField(
        'Round Blog Image',
    )

    def validate_blog_image(self, field):
        try:
            r = requests.get(self.blog_image.data, stream=True)
            if r.status_code == 200:
                if not imghdr.what("image", h=r.content):
                    raise ValidationError("Not a supported image type or not an image at all")
            else:
                raise ValidationError("URL is not accessible")
        except:
            raise ValidationError("The url or the image it points to is invalid")

