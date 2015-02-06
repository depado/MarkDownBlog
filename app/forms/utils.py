# -*- coding: utf-8 -*-

import requests
import imghdr

from wtforms import ValidationError


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
