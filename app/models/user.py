# -*- coding: utf-8 -*-

from datetime import datetime
from slugify import slugify
from sqlalchemy import desc
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin.contrib.sqla import ModelView

from app.models import AuthMixin, Post
from app import app, db, login_manager

SYNTAX_HIGHLIGHTER_CHOICES = [
    'autumn.css', 'borland.css', 'bw.css', 'colorful.css', 'default.css', 'emacs.css', 'friendly.css', 'fruity.css',
    'github.css', 'manni.css', 'monokai.css', 'murphy.css', 'native.css', 'pastie.css', 'perldoc.css', 'tango.css',
    'trac.css', 'vim.css', 'vs.css', 'zenburn.css'
]
SYNTAX_HIGHLIGHTER_TUPLE = [(raw, raw.capitalize()[:-4]) for raw in SYNTAX_HIGHLIGHTER_CHOICES]


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

    # Blog Related Informations
    blog_slug = db.Column(db.String(50), unique=True)
    blog_title = db.Column(db.String(50), default="Untitled Blog")
    blog_description = db.Column(db.String(200), default="No Description")
    blog_public = db.Column(db.Boolean(), default=True)

    # Blog Images Related
    blog_image = db.Column(db.String(200))
    blog_image_rounded = db.Column(db.Boolean(), default=False)
    blog_bg = db.Column(db.String(200))
    blog_bg_public = db.Column(db.Boolean(), default=False)
    blog_bg_repeat = db.Column(db.Boolean(), default=False)
    blog_bg_everywhere = db.Column(db.Boolean(), default=False)
    blog_bg_override = db.Column(db.Boolean(), default=False)

    # Blog Pagination
    blog_paginate = db.Column(db.Boolean(), default=False)
    blog_paginate_by = db.Column(db.Integer(), default=10)

    # Blog Design
    blog_truncate_posts = db.Column(db.Boolean(), default=False)
    blog_syntax_highlighter_css = db.Column(db.Enum(*SYNTAX_HIGHLIGHTER_CHOICES), default='monokai.css')

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, active=True, superuser=False, api_purpose=False, **kwargs):
        """
        :param username: The username of the user, will become the blog subdomain once slugified.
        :param password: The raw password to be encrypted and stored.
        :param active: To change once postfix is setup and app can send mails.
        :param superuser: Set if the user is a superuser (currently no use for that)
        :param api_purpose: If using this with Marshmallow, do not bother to generate a password.
        """
        super(User, self).__init__(active=active, superuser=superuser, **kwargs)
        now = datetime.utcnow()
        if not api_purpose:
            self.set_password(self.password)
        self.register_date = now
        self.last_login = now
        self.blog_slug = slugify(self.username)

    @property
    def total_pages(self):
        """
        Property that returns the minimum number of pages to display all the articles (posts)
        :return: int
        """
        count = self.posts.count()
        if count % self.blog_paginate_by == 0:
            return int(count / self.blog_paginate_by)
        else:
            return int(count / self.blog_paginate_by) + 1

    @property
    def pages_as_list(self):
        """
        Returns a list of integers representing the available pages
        """
        return list(range(1, self.total_pages + 1))

    def get_page(self, page):
        if not page < self.total_pages:
            return None
        else:
            return list(self.posts.order_by(desc(Post.pub_date)).all())[self.blog_paginate_by * page: self.blog_paginate_by * (page+1)]

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while saving a user")
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception("Something went wrong while deleting a user")
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

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


class UserView(AuthMixin, ModelView):

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
