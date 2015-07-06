# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, make_response, abort
from flask_login import current_user
from sqlalchemy import desc

from . import blueprint
from .utils import requested_blog_user, generate_background_css, blog_exists, generate_syntax_highlighter_css
from app.models import Post


@blueprint.route("/")
@blog_exists
def index(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user.blog_paginate:
        posts = blog_user.get_page(0)
        current_page = 1
        return render_template("blog/blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               syntax_highlighter_css=generate_syntax_highlighter_css(blog_user),
                               paginate=True, current_page=current_page, **generate_background_css(blog_user))
    else:
        posts = blog_user.posts.order_by(desc(Post.pub_date)).all()
        return render_template("blog/blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               syntax_highlighter_css=generate_syntax_highlighter_css(blog_user),
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
        return render_template("blog/blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user,
                               paginate=True, current_page=current_page,
                               syntax_highlighter_css=generate_syntax_highlighter_css(blog_user),
                               **generate_background_css(blog_user))


@blueprint.route("/<post_slug>")
@blog_exists
def get(user_slug, post_slug):
    blog_user = requested_blog_user(user_slug)
    post = Post.query.filter_by(title_slug=post_slug).first()
    if post is not None:
        return render_template("blog/blog_page.html", post=post, owner=blog_user == current_user, blog_user=blog_user,
                               syntax_highlighter_css=generate_syntax_highlighter_css(blog_user),
                               **generate_background_css(blog_user))
    else:
        return render_template("blog/blog_page_404.html")


@blueprint.route("/<post_slug>/raw")
@blog_exists
def get_raw(user_slug, post_slug):
    post = Post.query.filter_by(title_slug=post_slug).first()
    if post is not None:
        resp = make_response(post.content)
        resp.mimetype = 'text/plain'
        return resp
    else:
        abort(404)


@blueprint.route("/<post_slug>/ansi")
@blog_exists
def get_ansi(user_slug, post_slug):
    post = Post.query.filter_by(title_slug=post_slug).first()
    if post is not None:
        resp = make_response(post.content_as_ansi())
        resp.mimetype = 'text/plain'
        resp.charset = 'utf-8'
        return resp
    else:
        abort(404)


@blueprint.route("/all")
@blog_exists
def all_posts(user_slug):
    blog_user = requested_blog_user(user_slug)
    posts = blog_user.get_all_posts()
    return render_template("blog/blog_all_posts.html", posts=posts, owner=blog_user == current_user,
                           blog_user=blog_user, syntax_highlighter_css=generate_background_css(blog_user),
                           **generate_background_css(blog_user))
