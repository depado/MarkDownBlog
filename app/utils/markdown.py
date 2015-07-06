# -*- coding: utf-8 -*-

import misaka
from misaka import HtmlRenderer, SmartyPants, BaseRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.formatters.terminal256 import Terminal256Formatter


class AnsiRenderer(BaseRenderer):

    def block_quote(self, quote):
        return "{}\n\n".format(quote)

    def block_html(self, raw_html):
        return "{}\n\n".format(raw_html)

    def header(self, text, level):
        border = '-'
        if level == 1:
            border = '='

        return "\n\x1b[31;1m{border}\n| {text} |\n{border}\n\x1b[0m\n".format(border=border*(len(text)+4), text=text)

    def hrule(self):
        return "----------\n\n"

    def list(self, contents, is_ordered):
        return "{}\n".format(contents)

    def list_item(self, text, is_ordered):
        return "- {}\n".format(text)

    def paragraph(self, text):
        return "{}\n\n".format(text)

    def autolink(self, link, is_email):
        return link

    def codespan(self, code):
        return code

    def double_emphasis(self, text):
        return text

    def emphasis(self, text):
        return text

    def image(self, link, title, alt_text):
        return link

    def linebreak(self):
        return "\n"

    def link(self, link, title, content):
        return link

    def raw_html(self, raw_html):
        return raw_html

    def triple_emphasis(self, text):
        return text

    def strikethrough(self, text):
        return text

    def superscript(self, text):
        return text

    def block_code(self, text, lang):
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)

        formatter = Terminal256Formatter()
        return "{formatted}\n".format(
            formatted=highlight(text, lexer, formatter),
        )

ansi_renderer = misaka.Markdown(
    AnsiRenderer(),
    extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS
)

class HighlighterRenderer(HtmlRenderer, SmartyPants):

    def block_code(self, text, lang):
        has_syntax_highlite = False
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            if lang != 'text':
                has_syntax_highlite = True
        except:
            lexer = get_lexer_by_name('text', stripall=True)

        formatter = HtmlFormatter()
        return "{open_block}{formatted}{close_block}".format(
            open_block="<div class='code-highlight'>" if has_syntax_highlite else '',
            formatted=highlight(text, lexer, formatter),
            close_block="</div>" if has_syntax_highlite else ''
        )

    def table(self, header, body):
        return "<table class='table table-bordered table-hover'>" + header + body + "</table>"

markdown_renderer = misaka.Markdown(
    HighlighterRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK),
    extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_AUTOLINK | misaka.EXT_SPACE_HEADERS | misaka.EXT_STRIKETHROUGH | misaka.EXT_SUPERSCRIPT
)
