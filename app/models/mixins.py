# -*- coding: utf-8 -*-

from flask_login import current_user


class AuthMixin(object):
    def is_accessible(self):
        if not current_user.is_anonymous():
            if current_user.is_superuser():
                return True
        return False
