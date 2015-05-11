# -*- coding: utf-8 -*-

from flask import g, request

from flask_restless import ProcessingException

from app.models import User


def auth_required(data=None, **kwargs):
    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
    elif data and 'token' in data:
        token = data.pop('token', None)
    else:
        raise ProcessingException(description="Authorization Token Required", code=401)
    user = User.verify_auth_token(token)
    if not user:
        raise ProcessingException(description="Invalid Authorization Token", code=401)
    g.user = user
