# -*- coding: utf-8 -*-

from flask import url_for
from flask_login import current_user

from app import app

def generate_bg_css():
    repeat_mode = "no-repeat"
    background_cover = True
    backgroud_css_template = "background: url('{background_url}') {repeat_mode} center center fixed;"
    background_url = url_for('static', filename='img/bg.jpg')
    if current_user.is_authenticated():
        if current_user.blog_bg and current_user.blog_bg_everywhere:
            background_url = current_user.blog_bg
            if current_user.blog_bg_repeat:
                repeat_mode = "repeat"
                background_cover = False
    background_css = backgroud_css_template.format(background_url=background_url, repeat_mode=repeat_mode)
    return dict(background_css=background_css, background_cover=background_cover)


@app.context_processor
def inject_user():
    return dict(user=current_user)

@app.context_processor
def inject_background_css():
    return generate_bg_css()
