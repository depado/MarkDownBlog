# -*- coding: utf-8 -*-

from sqlalchemy import desc
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from jinja2 import utils

from app.models import User, Post

blueprint = Blueprint('blog', __name__, subdomain="<user_slug>")


def requested_blog_user(user_slug):
    return User.query.filter_by(blog_slug=user_slug).first()


@blueprint.route("/")
def index(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        posts = blog_user.posts.order_by(desc(Post.pub_date)).all()
        return render_template("blog_index.html", owner=blog_user == current_user, posts=posts, blog_user=blog_user)
    else:
        return render_template("blog_404.html", blog_name=utils.escape(user_slug))


@blueprint.route("/<int:post_id>")
def get(user_slug, post_id):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        post = Post.query.get(post_id)
        if post is not None:
            return render_template("blog_page.html", post=post, owner=blog_user == current_user, blog_user=blog_user)
        else:
            return render_template("blog_page_404.html", post_id=post_id)
    else:
        return render_template("blog_404.html", blog_name=utils.escape(user_slug))
