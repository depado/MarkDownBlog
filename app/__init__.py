# -*- coding: utf-8 -*-

from flask import Flask
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView, expose

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


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


