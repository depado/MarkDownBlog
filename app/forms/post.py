# -*- coding: utf-8 -*-

from slugify import slugify
from datetime import datetime

from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError

from flask_login import current_user

from .base import CustomForm
from app.models import Post


class NewPostForm(CustomForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)], description={'placeholder': "Title"})
    content = TextAreaField('Post', validators=[DataRequired()], description={'placeholder': "Content (MarkDown)"})

    def validate_title(self, field):
        slugged = slugify("{date}-{title}".format(date=str(datetime.utcnow().date()), title=self.title.data))
        if Post.query.filter_by(user=current_user, title_slug=slugged).first() is not None:
            raise ValidationError("You already posted an article with the same title today. "
                                  "(To prevent spam and inaccessible articles, you can't do that.)")


class EditPostForm(CustomForm):
    """
    The Edition form. Disable the field validation to perform it manually on the instance.
    """
    title = StringField('Title', validators=[DataRequired(), Length(min=5)], description={'placeholder': "Title"})
    content = TextAreaField('Post', validators=[DataRequired()], description={'placeholder': "Content (MarkDown)"})
