# -*- coding: utf-8 -*-

from datetime import datetime

from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView

from app.models import AuthMixin
from app import db, login_manager


class User(db.Model):
    """
    Simple User model. Integrates with Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(54))
    superuser = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    register_date = db.Column(db.DateTime())

    blog_slug = db.Column(db.String(50), unique=True)

    blog_title = db.Column(db.String(50))
    blog_description = db.Column(db.String(200))
    blog_image = db.Column(db.String(200))
    blog_round_image = db.Column(db.Boolean())

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, password, active=True, superuser=False):
        self.username = username
        self.superuser = superuser
        self.active = active
        self.set_password(password)
        self.blog_slug = slugify(self.username)
        self.register_date = datetime.utcnow()
        self.blog_title = "Untitled Blog"
        self.blog_description = "No Description"
        self.blog_image = ""
        self.blog_round_image = False

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        return True

    def is_superuser(self):
        return self.superuser

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.username

    def __unicode__(self):
        return self.username


class UserView(AuthMixin, ModelView):

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
