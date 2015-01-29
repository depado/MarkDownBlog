# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required

from app import app
from app.models import Post
from app.forms import PostForm

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PostForm(request.form, prefix="post")
    if form.has_been_submitted(request):
        if form.validate_on_submit():
            new_post = Post(user=current_user, title=form.title.data, content=form.content.data)
            status = new_post.save()
            if status:
                flash("Successfully posted the article")
                return redirect(url_for('blog.index', user_slug=current_user.blog_slug))
            else:
                flash("Something went wrong...", category="error")

    return render_template("new_post.html", form=form)

