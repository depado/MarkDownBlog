# -*- coding: utf-8 -*-

from sqlalchemy import desc
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user
from jinja2 import utils
from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed

from app.models import User, Post

blueprint = Blueprint('blog', __name__, subdomain="<user_slug>")


def make_external(url):
    return urljoin(request.url_root, url)


def requested_blog_user(user_slug):
    return User.query.filter_by(blog_slug=user_slug).first()


def generate_background_css(blog_user=None):
    chosen = None
    repeat_mode = "no-repeat"
    background_cover = True
    backgroud_css_template = "background: url('{background_url}') {repeat_mode} center center fixed;"
    background_url = url_for('static', filename='img/2.png')

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


@blueprint.route("/recent.atom")
def rss_feed(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        feed = AtomFeed(
            '{user} Recent Articles'.format(user=blog_user.username),
            feed_url=request.url,
            url=request.url_root
        )
        posts = blog_user.posts.order_by(desc(Post.pub_date)).limit(15).all()
        for post in posts:
            feed.add(post.title, post.content_as_html(),
                     content_type='html',
                     author=post.user.username,
                     url=make_external(url_for("blog.get", user_slug=user_slug, post_slug=post.title_slug)),
                     updated=post.pub_date,
                     published=post.pub_date)
        return feed.get_response()
    else:
        return ""



@blueprint.route("/")
def index(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        if blog_user.blog_paginate:
            posts = blog_user.get_page(0)
            current_page = 1
            return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                                   paginate=True, current_page=current_page, **generate_background_css(blog_user))
        else:
            posts = blog_user.posts.order_by(desc(Post.pub_date)).all()
            return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                                   **generate_background_css(blog_user))
    else:
        return render_template("blog_404.html", blog_name=utils.escape(user_slug))


@blueprint.route("/<int:page>")
def page(user_slug, page):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        if not blog_user.blog_paginate or page <= 1:
            return redirect(url_for("blog.index", user_slug=user_slug))
        else:
            posts = blog_user.get_page(page - 1)
            if posts is None:
                return redirect(url_for("blog.index", user_slug=user_slug))
            current_page = page
            return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                                   paginate=True, current_page=current_page, **generate_background_css(blog_user))
    else:
        return render_template("blog_404.html", blog_name=utils.escape(user_slug))


@blueprint.route("/<post_slug>")
def get(user_slug, post_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        post = Post.query.filter_by(title_slug=post_slug).first()
        if post is not None:
            return render_template("blog_page.html", post=post, owner=blog_user == current_user, blog_user=blog_user,
                                   **generate_background_css(blog_user))
        else:
            return render_template("blog_page_404.html")
    else:
        return render_template("blog_404.html", blog_name=utils.escape(user_slug))
