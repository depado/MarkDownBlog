# -*- coding: utf-8 -*-

from flask_login import current_user


class AuthMixin(object):
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_superuser
