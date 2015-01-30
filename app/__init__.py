# -*- coding: utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_misaka import Misaka

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

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

@app.context_processor
def inject_user():
    return dict(user=current_user)


