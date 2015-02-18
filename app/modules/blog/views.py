# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask_login import current_user
from sqlalchemy import desc

from . import blueprint
from .utils import requested_blog_user, generate_background_css, blog_exists
from app.models import Post


@blueprint.route("/")
@blog_exists
def index(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user.blog_paginate:
        posts = blog_user.get_page(0)
        current_page = 1
        return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               paginate=True, current_page=current_page, **generate_background_css(blog_user))
    else:
        posts = blog_user.posts.order_by(desc(Post.pub_date)).all()
        return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               **generate_background_css(blog_user))


@blueprint.route("/<int:page>")
@blog_exists
def page(user_slug, page):
    blog_user = requested_blog_user(user_slug)
    if not blog_user.blog_paginate or page <= 1:
        return redirect(url_for("blog.index", user_slug=user_slug))
    else:
        posts = blog_user.get_page(page - 1)
        if posts is None:
            return redirect(url_for("blog.index", user_slug=user_slug))
        current_page = page
        return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               paginate=True, current_page=current_page, **generate_background_css(blog_user))


@blueprint.route("/<post_slug>")
@blog_exists
def get(user_slug, post_slug):
    blog_user = requested_blog_user(user_slug)
    post = Post.query.filter_by(title_slug=post_slug).first()
    if post is not None:
        return render_template("blog_page.html", post=post, owner=blog_user == current_user, blog_user=blog_user,
                               **generate_background_css(blog_user))
    else:
        return render_template("blog_page_404.html")
