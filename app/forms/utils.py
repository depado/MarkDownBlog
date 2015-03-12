# -*- coding: utf-8 -*-

import requests
import imghdr
from datetime import datetime
from slugify import slugify

from wtforms import ValidationError
from flask_login import current_user

from app.models import Post


class ImageUrl(object):

    def __call__(self, form, field):
        try:
            r = requests.get(field.data, stream=True)
            if r.status_code == 200:
                if not imghdr.what("image", h=r.content):
                    raise ValidationError("Not a supported image type or not an image at all")
            else:
                raise ValidationError("URL is not accessible")
        except:
            raise ValidationError("The url or the image it points to is invalid")


def validate_post_title(title):
    """
    Returns whether a title is valid or not.
    :param title: The title of the post
    :return: Boolean
    """
    slugged = slugify("{date}-{title}".format(date=str(datetime.utcnow().date()), title=title))
    return Post.query.filter_by(user=current_user, title_slug=slugged).first() is None
