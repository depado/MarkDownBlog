# -*- coding: utf-8 -*-

from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import app
from app.forms import SettingForm, ChangePasswordForm

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm(obj=current_user)
    change_pwd_form = ChangePasswordForm(prefix='pwd')

    if form.has_been_submitted(request):
        print("Not supposed to be here")
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
            current_user.blog_public = form.blog_public.data
            current_user.blog_truncate_posts = form.blog_truncate_posts.data
            current_user.blog_syntax_highlighter_css = form.blog_syntax_highlighter_css.data
            current_user.linkedin_url = form.linkedin_url.data
            current_user.gplus_url = form.gplus_url.data
            current_user.github_url = form.github_url.data
            current_user.twitter_url = form.twitter_url.data
            saved = current_user.save()
            if saved:
                flash("Saved your settings.")
                return redirect(url_for("blog.index", user_slug=current_user.blog_slug))
            else:
                flash("Something went wrong...")

    elif change_pwd_form.has_been_submitted(request):
        if change_pwd_form.validate_on_submit():
            current_user.set_password(change_pwd_form.new_password.data)
            saved = current_user.save()
            if saved:
                flash("Changed your password.")
            else:
                flash("Something went wrong...")

    return render_template("settings.html", form=form, change_pwd_form=change_pwd_form)
