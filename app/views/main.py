# -*- coding: utf-8 -*-

from sqlalchemy import desc
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm, RegisterForm
from app.models import User


def has_been_submitted(form, request):
    return request.method == "POST" and request.form['btn'] == "{}btn".format(getattr(form, "_prefix"))


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    TODO: Handle if user is connected
    start_div is the div displayed on page load. Useful for forms with errors
    """
    if current_user.is_authenticated():
        latest_users = User.query.order_by(desc(User.register_date)).limit(10).all()
        return render_template("blog_explore.html", latest_users=latest_users)

    start_div = "home-div"
    login_form = LoginForm(request.form, prefix="login")
    register_form = RegisterForm(request.form, prefix="register")

    if login_form.has_been_submitted(request):
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            login_user(user)
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
