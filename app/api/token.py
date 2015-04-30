# -*- coding: utf-8 -*-

from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth

from app import app, db
from app.models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True

@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
