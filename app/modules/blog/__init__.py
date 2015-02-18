# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint('blog', __name__, subdomain="<user_slug>")

from .rss import rss_feed
from .views import get, index, page
