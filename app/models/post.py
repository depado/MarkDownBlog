# -*- coding: utf-8 -*-

from datetime import datetime

from app.utils import markdown_renderer

from app import app, db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.UnicodeText)
    pub_date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, title, content, pub_date=None):
        self.user = user
        self.title = title
        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except:
            app.logger.exception("Something went wrong while saving a post")
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except:
            app.logger.exception("Something went wrong while deleting a post")
            db.session.rollback()
            return False
        return True

    def content_as_html(self):
        return markdown_renderer.render(self.content)
