# -*- coding: utf-8 -*-

from flask import request, url_for
from sqlalchemy import desc
from werkzeug.contrib.atom import AtomFeed

from . import blueprint
from .utils import requested_blog_user, make_external
from app.models import Post


@blueprint.route("/recent.atom")
def rss_feed(user_slug):
    blog_user = requested_blog_user(user_slug)
    if blog_user:
        feed = AtomFeed(
            '{user} Recent Articles'.format(user=blog_user.username),
            feed_url=request.url,
            url=request.url_root
        )
        posts = blog_user.posts.order_by(desc(Post.pub_date)).limit(15).all()
        for post in posts:
            feed.add(post.title, post.content_as_html(),
                     content_type='html',
                     author=post.user.username,
                     url=make_external(url_for("blog.get", user_slug=user_slug, post_slug=post.title_slug)),
                     updated=post.pub_date,
                     published=post.pub_date)
        return feed.get_response()
    else:
        return ""
