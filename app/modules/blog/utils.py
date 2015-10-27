# -*- coding: utf-8 -*-

import functools
from urllib.parse import urljoin

from flask import url_for, request, render_template
from flask_login import current_user
from jinja2 import utils

from app.models import User


def make_external(url):
    return urljoin(request.url_root, url)


def requested_blog_user(user_slug):
    return User.query.filter_by(blog_slug=user_slug).first()


def generate_background_css(blog_user=None):
    chosen = None
    repeat_mode = "no-repeat"
    background_cover = True
    backgroud_css_template = "background: url('{background_url}') {repeat_mode} center center fixed;"
    background_url = url_for('static', filename='img/bg.jpg')

    if blog_user:
        if blog_user.blog_bg and blog_user.blog_bg_public:
            if current_user.is_authenticated() and current_user.blog_bg and current_user.blog_bg_override:
                chosen = current_user
            else:
                chosen = blog_user
    else:
        if current_user.is_authenticated() and current_user.blog_bg and current_user.blog_bg_everywhere:
            chosen = current_user

    if chosen:
        background_url = chosen.blog_bg
        if chosen.blog_bg_repeat:
            repeat_mode = "repeat"
            background_cover = False
    background_css = backgroud_css_template.format(background_url=background_url, repeat_mode=repeat_mode)
    return dict(background_css=background_css, background_cover=background_cover)


def generate_syntax_highlighter_css(blog_user=None):
    if blog_user:
        return url_for("static", filename="css/syntax/{}".format(blog_user.blog_syntax_highlighter_css))


def blog_exists(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        user_slug = kwargs.get('user_slug', None)
        if user_slug:
            blog_user = requested_blog_user(user_slug)
            if not blog_user:
                return render_template("blog_404.html", blog_name=utils.escape(user_slug))
        return f(*args, **kwargs)
    return decorated_function
