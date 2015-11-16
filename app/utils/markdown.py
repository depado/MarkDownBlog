# -*- coding: utf-8 -*-

import re

import mistune
import misaka
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.formatters.terminal256 import Terminal256Formatter


class AnsiRenderer(misaka.BaseRenderer):

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


class MathBlockGrammar(mistune.BlockGrammar):
    block_math = re.compile(r"^\$\$(.*?)\$\$", re.DOTALL)
    latex_environment = re.compile(r"^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}", re.DOTALL)


class MathBlockLexer(mistune.BlockLexer):
    default_rules = ['block_math', 'latex_environment'] + mistune.BlockLexer.default_rules

    def __init__(self, rules=None, **kwargs):
        if rules is None:
            rules = MathBlockGrammar()
        super(MathBlockLexer, self).__init__(rules, **kwargs)

    def parse_block_math(self, m):
        """Parse a $$math$$ block"""
        self.tokens.append({
            'type': 'block_math',
            'text': m.group(1)
        })

    def parse_latex_environment(self, m):
        self.tokens.append({
            'type': 'latex_environment',
            'name': m.group(1),
            'text': m.group(2)
        })


class MathInlineGrammar(mistune.InlineGrammar):
    math = re.compile(r"^\$(.+?)\$", re.DOTALL)
    block_math = re.compile(r"^\$\$(.+?)\$\$", re.DOTALL)
    text = re.compile(r'^[\s\S]+?(?=[\\<!\[_*`~$]|https?://| {2,}\n|$)')


class MathInlineLexer(mistune.InlineLexer):
    default_rules = ['block_math', 'math'] + mistune.InlineLexer.default_rules

    def __init__(self, renderer, rules=None, **kwargs):
        if rules is None:
            rules = MathInlineGrammar()
        super(MathInlineLexer, self).__init__(renderer, rules, **kwargs)

    def output_math(self, m):
        return self.renderer.inline_math(m.group(1))

    def output_block_math(self, m):
        return self.renderer.block_math(m.group(1))


class MarkdownWithMath(mistune.Markdown):
    def __init__(self, renderer, **kwargs):
        if 'inline' not in kwargs:
            kwargs['inline'] = MathInlineLexer
        if 'block' not in kwargs:
            kwargs['block'] = MathBlockLexer
        super(MarkdownWithMath, self).__init__(renderer, **kwargs)

    def output_block_math(self):
        return self.renderer.block_math(self.token['text'])

    def output_latex_environment(self):
        return self.renderer.latex_environment(self.token['name'], self.token['text'])


class HighlighterRenderer(mistune.Renderer):

    def __init__(self, *args, **kwargs):
        super(HighlighterRenderer, self).__init__(*args, **kwargs)
        self.toc_count = 0
        self.toc_tree = []

    def block_code(self, code, lang=None):
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()
        return "{open_block}{formatted}{close_block}".format(
            open_block="<div class='code-highlight'>" if lang != 'text' else '',
            formatted=highlight(code, lexer, formatter),
            close_block="</div>" if lang != 'text' else ''
        )

    def table(self, header, body):
        return "<table class='table table-bordered table-hover'>" + header + body + "</table>"

    def image(self, src, title, text):
        if src.startswith('javascript:'):
            src = ''
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img class="img-responsive center-block" src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img class="img-responsive center-block" src="%s" alt="%s"' % (src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

    # Pass math through unaltered - mathjax does the rendering in the browser
    def block_math(self, text):
        return '$$%s$$' % text

    def latex_environment(self, name, text):
        return r'\begin{%s}%s\end{%s}' % (name, text, name)

    def inline_math(self, text):
        return '$%s$' % text

    def reset_toc(self):
        self.toc_tree = []
        self.toc_count = 0

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def render_toc(self, level=3):
        """Render TOC to HTML.
        :param level: render toc to the given level
        """
        print(self.toc_count)
        return ''.join(self._iter_toc(level))

    def _iter_toc(self, level):
        first_level = None
        last_level = None

        yield '<ul id="table-of-content">\n'

        for toc in self.toc_tree:
            index, text, l, raw = toc

            if l > level:
                # ignore this level
                continue

            if first_level is None:
                # based on first level
                first_level = l
                last_level = l
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l:
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l - 1:
                last_level = l
                yield '<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level > l:
                # close indention
                yield '</li>'
                while last_level > l:
                    yield '</ul>\n</li>\n'
                    last_level -= 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        if last_level and first_level:
            yield '</li>\n'
            while last_level > first_level:
                yield '</ul>\n</li>\n'
                last_level -= 1

        yield '</ul>\n'

renderer = HighlighterRenderer(escape=False)
markdown_renderer = MarkdownWithMath(renderer=renderer)
