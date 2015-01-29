# -*- coding: utf-8 -*-

from sqlalchemy import desc
from flask import render_template

from app import app
from app.models import User


@app.route("/explore")
def explore():
    latest_users = User.query.order_by(desc(User.register_date)).limit(10).all()
    return render_template("blog_explore.html", latest_users=latest_users)
