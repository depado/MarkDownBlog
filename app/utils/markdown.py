# -*- coding: utf-8 -*-

import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


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
