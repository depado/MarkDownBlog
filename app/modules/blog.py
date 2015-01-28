# -*- coding: utf-8 -*-

from flask import Blueprint

from app.models import User

blueprint = Blueprint('blog', __name__, subdomain="<user>")


def requested_blog_user(user):
    return User.query.filter_by(username=user).first()


@blueprint.route("/")
def index(user):
    # Compare if logged_user has the login and return admin page otherwise blog entries
    blog_user = requested_blog_user(user)
    if blog_user:
        return "{} blog there".format(user)
    else:
        return "{} blog not found".format(user)


@blueprint.route("/<int:id>")
def get(user, id):
    # Compare too
    blog_user = requested_blog_user(user)
    if blog_user:
        return "{} blog {} entry".format(user, id)
    else:
        return "{} blog not found babe".format(user)
