# -*- coding: utf-8 -*-

from datetime import datetime

from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from app import app, db
from app.models import User, Post

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True


@app.route('/curl/post', methods=['POST'])
@auth.login_required
def curl_post():
    try:
        content = request.json.get('content')
        title = request.json.get('title')
        post = Post(user=g.user, title=title, content=content, pub_date=datetime.now())
        post.save()
        return jsonify({'data': 'Hello, %s!' % g.user.username})
    except:
        return jsonify({'data': 'Something Went Wrong.'})
