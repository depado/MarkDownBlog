# -*- coding: utf-8 -*-

from datetime import datetime
from slugify import slugify
from bs4 import BeautifulSoup

from flask import url_for
from flask_login import current_user

from app import app, db
from app.utils import markdown_renderer, ansi_renderer


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    title_slug = db.Column(db.String(200))
    content = db.Column(db.UnicodeText)
    pub_date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        self.pub_date = self.pub_date if self.pub_date is not None else datetime.utcnow()
        self.set_title_slug()

    def set_title_slug(self):
        self.title_slug = slugify("{date}-{title}".format(date=str(self.pub_date.date()), title=self.title))

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while saving a post")
            db.session.rollback()
            return False
        return True

    def owner(self):
        return current_user == self.user

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while deleting a post")
            db.session.rollback()
            return False
        return True

    def content_as_html(self, index=False):
        if self.user.blog_truncate_posts and index:
            content = markdown_renderer.render(self.content)
            try:
                truncated = content[:300 + content[300:].index(" ")]
                truncate_end = " [...]<br / ><a href='{url}'>Click here to read the full article</a>".format(
                    url=url_for('blog.get', user_slug=self.user.blog_slug, post_slug=self.title_slug)
                )
                return BeautifulSoup(truncated + truncate_end)
            except Exception as e:
                return content
        else:
            return markdown_renderer.render(self.content)

    def content_as_ansi(self):
        return ansi_renderer.render(self.content)
