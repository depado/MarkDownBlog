# -*- coding: utf-8 -*-

from sqlalchemy import desc
from flask import render_template

from app import app
from app.models import User, Post


def explore_context():
    latest_users = User.query.order_by(desc(User.register_date)).limit(10).all()
    posts = Post.query.join(User).filter(User.blog_public).order_by(desc(Post.pub_date)).limit(10).all()
    return dict(posts=posts, latest_users=latest_users)


@app.route("/explore")
def explore():
    return render_template("blog_explore.html", **explore_context())


@app.route("/all")
def explore_all():
    posts = Post.query.join(User).filter(User.blog_public).order_by(desc(Post.pub_date)).all()
    return render_template("blog_explore_all.html", posts=posts)
