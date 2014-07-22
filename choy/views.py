# coding:utf8
"""

Author: ilcwd
"""
import flask
from choy import init, models


@init.application.route('/')
@init.application.route('/a/')
@init.application.route('/a/<path:path>')
def show_article(path=''):
    menus = models.get_menus()
    title, article = models.get_article(path)

    context = dict(
        menus=menus,
        title=title,
        article=article,
    )

    return flask.render_template('base.html', **context)


@init.application.route('/ping')
def ping():
    return 'pong'

@init.application.route('/favicon.ico')
def favicon():
    basefolder = init.CONFIG.BASE_FOLDER

    return flask.send_from_directory(basefolder, 'favicon.ico')

@init.application.errorhandler(404)
def error_404(e):
    return '404'