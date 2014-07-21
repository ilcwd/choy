# coding:utf8
"""

Author: ilcwd
"""
import os

import markdown

from markdownblog.init import config


class Menu(object):
    def __init__(self, name, url, children=None):
        self.name = name
        self.url = url
        self.children = children or []


def markdown2html(source):
    exts = [
        'markdown.extensions.admonition',
        'markdown.extensions.toc',
    ]
    md = markdown.Markdown(output_format='html5', extensions=exts)
    content = md.convert(source)
    return content


def get_blog(path):
    realpath = os.path.join(config['base_folder'], path)
    print realpath

    title = os.path.split(path)[-1]

    if os.path.exists(path) and os.path.isdir(realpath):
        # target is a direcoty, try get its `index.md`

        realpath = os.path.join(realpath, 'index.md')
        if not os.path.exists(realpath):
            return title, None
    else:
        realpath += '.md'

    with open(realpath, 'r') as fp:
        content = markdown2html(fp.read())

    return title, content


def get_menus():
    return [
        Menu('你好', '#', [Menu('Hello111', '#'), Menu('Hello222', '#', [Menu('Hello333', '#'), Menu('Hello444', '#', )])]),
        Menu('Hello', '#'),
        Menu('阿隆索打飞机<>dd拉萨京东方了', '#'),
    ]

