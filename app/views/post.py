# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required

from app import app
from app.models import Post
from app.forms import NewPostForm, EditPostForm
from app.forms.utils import validate_post_title
from app.utils import markdown_renderer
from app.modules.blog.utils import generate_syntax_highlighter_css


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = NewPostForm(request.form, prefix="post")
    if form.has_been_submitted(request):
        if form.validate_on_submit():
            new_post = Post(user=current_user, title=form.title.data, content=form.content.data)
            status = new_post.save()
            if status:
                flash("Successfully posted the article")
                return redirect(url_for('blog.index', user_slug=current_user.blog_slug))
            else:
                flash("Something went wrong...", category="error")

    return render_template("new_post.html", form=form,
                           syntax_highlighter_css=generate_syntax_highlighter_css(current_user))


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get(post_id)
    if post is not None:
        if post.user == current_user:
            form = EditPostForm(obj=post)
            if form.has_been_submitted(request) and form.validate_on_submit():

                if post.title != form.title.data and not validate_post_title(form.title.data):
                    form.title.errors.append("You already posted an article with the same title today.")
                    return render_template("edit_post.html", form=form)

                post.title = form.title.data
                post.content = form.content.data
                post.set_title_slug()
                saved = post.save()
                if saved:
                    flash("Successfully saved the post.")
                    return redirect(url_for("blog.get", user_slug=current_user.blog_slug, post_slug=post.title_slug))
                else:
                    flash("Something went wrong...")

            return render_template("edit_post.html", form=form,
                                   syntax_highlighter_css=generate_syntax_highlighter_css(current_user))
        else:
            # The user trying to edit is not the actual owner
            flash("Your are not authorized to do that.")
            return redirect(url_for('index'))
    else:
        # The post has not been found
        return render_template("blog_page_404", post_id=post_id)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Post.query.get(post_id)
    if post is not None:
        if post.user == current_user:
            deleted = post.delete()
            if deleted:
                flash("The article has been deleted.")
            else:
                flash("Something went wrong.")
            return redirect(url_for('blog.index', user_slug=post.user.blog_slug))
        else:
            flash("You don't have the permission to do that.")
            return redirect(url_for('blog.index', user_slug=post.user.blog_slug))
    else:
        return render_template("blog_page_404.html", post_id=post_id)


@app.route("/_parse", methods=['POST'])
def ajax_markdown_parser():
    return markdown_renderer.render(request.json)


