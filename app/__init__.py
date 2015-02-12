# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask_misaka import Misaka

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')
)
app.logger.addHandler(handler)

db = SQLAlchemy(app)
Misaka(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated():
            if current_user.is_superuser():
                return super(MyAdminIndexView, self).index()
        return redirect(url_for('MainView:index'))

admin = Admin(app, 'We Rate Movies', index_view=MyAdminIndexView())

from app import views, models

from app.modules import blog
app.register_blueprint(blog.blueprint)

from app.views.context import *


