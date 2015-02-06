# -*- coding: utf-8 -*-

from datetime import datetime

from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView

from app.models import AuthMixin
from app import db, login_manager


class User(db.Model):
    """
    User with blog model. Integrates with Flask-Login.

    id: The ID of the user.
    username: The username of the user (can contain any characters)
    password: Encrypted password
    superuser: Boolean to tell if the user is a superuser
    active: Boolean to tell if the user is active (ability to login and operate on the app)
    register_date: The date the user registered
    last_login: The date the user last logged in the app

    blog_slug: The slugified username. Used as subdomain
    blog_title: The title of the blog that can be set in the user's settings
    blog_description: The description of the blog that can be set in the user's settings
    blog_image: The image (avatar) of the blog that can be set in the user's settings using an URL
    blog_image_rounded: Tells whether the image of the blog should be rounded or not (user setting)

    blog_bg: The URL of the background of the user
    blog_bg_public: Tells if the background should be displayed to everyone or only the user
    blog_bg_repeat: Should the background be repeated ? Useful for small images
    blog_bg_everywhere: Use the background image everywhere on markdownblog instead of the default one
    blog_bg_override: Use the background everywhere even on other blogs

    posts: The posts associated to this blog/user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(54))
    superuser = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    register_date = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    blog_slug = db.Column(db.String(50), unique=True)
    blog_title = db.Column(db.String(50))
    blog_description = db.Column(db.String(200))
    blog_image = db.Column(db.String(200))
    blog_image_rounded = db.Column(db.Boolean())
    blog_bg = db.Column(db.String(200))
    blog_bg_public = db.Column(db.Boolean())
    blog_bg_repeat = db.Column(db.Boolean())
    blog_bg_everywhere = db.Column(db.Boolean())
    blog_bg_override = db.Column(db.Boolean())

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, password, active=True, superuser=False):
        """
        :param username: The username of the user, will become the blog subdomain once slugified.
        :param password: The raw password to be encrypted and stored.
        :param active: To change once postfix is setup and app can send mails.
        :param superuser: Set if the user is a superuser (currently no use for that)
        """
        now = datetime.utcnow()
        self.username = username
        self.superuser = superuser
        self.active = active
        self.set_password(password)
        self.register_date = now
        self.last_login = now

        self.blog_slug = slugify(self.username)
        self.blog_title = "Untitled Blog"
        self.blog_description = "No Description"

        self.blog_image = ""
        self.blog_image_rounded = False
        self.blog_bg = ""
        self.blog_bg_public = True
        self.blog_bg_repeat = False
        self.blog_bg_everywhere = False
        self.blog_bg_override = False

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
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
