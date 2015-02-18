# -*- coding: utf-8 -*-

from wtforms.fields import StringField, TextAreaField, BooleanField, IntegerField
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
        description={
            'help': "Do you want your blog image to be rounded ?"
        }
    )
    blog_public = BooleanField(
        'Public Blog',
        description={
            'help': "Can your articles be used on the explore/front page ?"
        }
    )
    blog_bg = StringField(
        'Blog Background',
        validators=[Optional(), URL(), ImageUrl()],
        description={'placeholder': "Blog Background"}
    )
    blog_bg_public = BooleanField(
        'Blog Background Public',
        description={
            'help': "Can the visitors of your blog see the background ?"
        }
    )
    blog_bg_repeat = BooleanField(
        'Blog Background Repeat',
        description={
            'help': "Activate if your image is small and you want it to be repeated in the background."
        }
    )
    blog_bg_everywhere = BooleanField(
        'Blog Background Everywhere',
        description={
            'help': "When you're logged-in, do you want this background to be applied everywhere on markdownblog ?"
        }
    )
    blog_bg_override = BooleanField(
        'Blog Background Override',
        description={
            'help': "When you're logged-in, do you want your own background to override the other blog's public background ?"
        }
    )
    blog_paginate = BooleanField(
        'Activate Pagination',
        description={
            'help': "Would you like to paginate your blog posts ?"
        }
    )
    blog_paginate_by = IntegerField(
        'Articles per Page',
        validators=[DataRequired("Even if not using pagination put a value here.")],
        description={'placeholder': "Articles per Page"}
    )

