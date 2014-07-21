# coding:utf8
"""

Author: ilcwd
"""
import flask
from markdownblog import init, misc


@init.application.route('/')
@init.application.route('/a/')
@init.application.route('/a/<path:path>')
def show_article(path=''):
    menus = misc.get_menus()
    title, content = misc.get_blog(path)

    context = dict(
        menus=menus,
        title=title,
        content=content,
    )

    return flask.render_template('base.html', **context)


@init.application.route('/ping')
def ping():
    return 'pong'