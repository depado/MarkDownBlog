# -*- coding: utf-8 -*-

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    post = db.Column(db.UnicodeText)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
