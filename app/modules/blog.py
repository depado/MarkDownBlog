# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import current_user
from jinja2 import utils

from app.models import User

blueprint = Blueprint('blog', __name__, subdomain="<user_slug>")


def requested_blog_user(user_slug):
    return User.query.filter_by(blog_slug=user_slug).first()


@blueprint.route("/")
def index(user_slug):
    # Compare if logged_user has the login and return admin page otherwise blog entries
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        return render_template("blog_index.html", user=current_user)
        #"{} blog there ({})<br />Blog Title : {}".format(blog_user.username, user_slug, blog_user.blog_title)
    else:
        return "{} blog not found".format(utils.escape(user_slug))


@blueprint.route("/<int:post_id>")
def get(user_slug, post_id):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        return "{} blog ({}) - {} entry".format(blog_user.username, user_slug, id)
    else:
        return "{} blog not found".format(user_slug)


@blueprint.route("/new")
def new(user_slug):
    return "Create"


@blueprint.route("/delete/<int:post_id>")
def delete(user_slug, post_id):
    return "Delete {}".format(post_id)


@blueprint.route("/settings")
def settings(user_slug):
    blog_user = requested_blog_user(user_slug)
    return "Settings"
