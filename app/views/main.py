# -*- coding: utf-8 -*-

from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.forms import LoginForm, RegisterForm, SettingForm
from app.models import User, Post
from app.views.explore import explore_context


def has_been_submitted(form, request):
    return request.method == "POST" and request.form['btn'] == "{}btn".format(getattr(form, "_prefix"))


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    TODO: Handle if user is connected
    start_div is the div displayed on page load. Useful for forms with errors
    """

    # Uncomment to force https on that page (maybe just for user login ?)
    # if not app.config['DEBUG']:  # and current_user.is_anonymous()
    #     if request.scheme == "http":
    #         return redirect(url_for("index", _scheme="https"))

    if current_user.is_authenticated():
        return render_template("blog_explore.html", **explore_context())

    start_div = "home-div"
    login_form = LoginForm(request.form, prefix="login")
    register_form = RegisterForm(request.form, prefix="register")

    if login_form.has_been_submitted(request):
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            login_user(user, remember=login_form.rememberme.data)
            user.last_login = datetime.now()
            user.save()
            flash("Your are now logged in.", category="info")
            return redirect(url_for('index'))
        else:
            start_div = "login-div"

    if register_form.has_been_submitted(request):
        if register_form.validate_on_submit():
            new_user = User(username=register_form.username.data, password=register_form.password.data, active=True,
                            superuser=False)
            new_user.save()
            return redirect(url_for('index'))
        else:
            start_div = "registration-div"

    return render_template("index.html", login_form=login_form, register_form=register_form, start_div=start_div)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm(obj=current_user)
    if form.has_been_submitted(request):
        if form.validate_on_submit():
            current_user.blog_title = form.blog_title.data
            current_user.blog_description = form.blog_description.data
            current_user.blog_image = form.blog_image.data
            current_user.blog_image_rounded = form.blog_image_rounded.data
            current_user.blog_bg = form.blog_bg.data
            current_user.blog_bg_public = form.blog_bg_public.data
            current_user.blog_bg_everywhere = form.blog_bg_everywhere.data
            current_user.blog_bg_override = form.blog_bg_override.data
            current_user.blog_bg_repeat = form.blog_bg_repeat.data
            current_user.blog_paginate = form.blog_paginate.data
            current_user.blog_paginate_by = form.blog_paginate_by.data
            saved = current_user.save()
            if saved:
                flash("Saved your settings...")
                return redirect(url_for("blog.index", user_slug=current_user.blog_slug))
            else:
                flash("Something went wrong...")
    return render_template("settings.html", form=form)
