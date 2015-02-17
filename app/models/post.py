# -*- coding: utf-8 -*-

from datetime import datetime
from slugify import slugify

from app import app, db
from app.utils import markdown_renderer


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    title_slug = db.Column(db.String(200))
    content = db.Column(db.UnicodeText)
    pub_date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, title, content, pub_date=None):
        self.user = user
        self.title = title
        self.title_slug = slugify(title)
        self.content = content
        self.pub_date = pub_date if pub_date is not None else datetime.utcnow()

    def save(self):
        self.title_slug = slugify("{date}-{title}".format(date=str(self.pub_date.date()), title=self.title))
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while saving a post")
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while deleting a post")
            db.session.rollback()
            return False
        return True

    def content_as_html(self):
        return markdown_renderer.render(self.content)
