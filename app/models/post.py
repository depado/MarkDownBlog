# -*- coding: utf-8 -*-

from datetime import datetime
import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from app import db


class HighlighterRenderer(HtmlRenderer, SmartyPants):

    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)

        formatter = HtmlFormatter(noclasses=True)
        s += highlight(text, lexer, formatter)
        return s

renderer = misaka.Markdown(
    HighlighterRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK),
    extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_AUTOLINK | misaka.EXT_SPACE_HEADERS | misaka.EXT_STRIKETHROUGH | misaka.EXT_SUPERSCRIPT
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.UnicodeText)
    pub_date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, title, content, pub_date=None):
        self.user = user
        self.title = title
        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            return False
        return True

    def content_as_html(self):
        return renderer.render(self.content)
