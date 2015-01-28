# -*- coding: utf-8 -*-

from flask import render_template

from app import app
from app.models import User


@app.route("/explore")
def explore():
    blogs = User.query.all()
    return render_template("explore.html")
