# coding:utf8
"""

Author: ilcwd
"""
import traceback
import re

import flask
import markdown


_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.admonition',
    'markdown.extensions.toc',
]
MARKDOWN_TITLE = 'title'
_RE_MATCH_HTML_H1 = re.compile(r"<h1(?P<attrs>[^>]*?)>(?P<title>.*?)</h1>", re.DOTALL)


def html_parse(source):
    msg = '<h1>Unsupported File Type</h1>'
    return {}, msg


def _read_html_h1(html):
    if not isinstance(html, (str, unicode)):
        return

    m = _RE_MATCH_HTML_H1.match(html)
    if m:
        return m.groupdict()['title']


def markdown_parse(source):
    exts = [
        'markdown.extensions.meta',
    ]
    exts.extend(_MARKDOWN_EXTENSIONS)
    md = markdown.Markdown(output_format='html5', extensions=exts)

    try:
        content = md.convert(source)
    except Exception as e:
        tb = traceback.format_exc()
        content = '''
        <h1>%s<h1>
        <code>
            %s
        </code>
        ''' % (flask.escape(str(e)), flask.escape(str(tb)))
        return {}, content

    # noinspection PyUnresolvedReferences
    meta = md.Meta.copy()
    if meta.get(MARKDOWN_TITLE):
        meta[MARKDOWN_TITLE] = meta[MARKDOWN_TITLE][0]
    else:
        meta[MARKDOWN_TITLE] = _read_html_h1(content)

    return meta, content