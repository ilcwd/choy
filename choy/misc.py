# coding:utf8
"""

Author: ilcwd
"""
import os
import traceback
import flask

import markdown

from choy.init import CONFIG


_INDEX_FILE = 'index.md'

_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.admonition',
    'markdown.extensions.toc',
]

_MARKDOWN_TITLE = 'title'


class Menu(object):
    def __init__(self, title, url, is_folder=False):
        self.title = title
        self.url = url
        self.is_folder = is_folder
        self.children = []


def _markdown_parse(source):
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
    if meta.get(_MARKDOWN_TITLE):
        meta[_MARKDOWN_TITLE] = meta[_MARKDOWN_TITLE][0]

    return meta, content


def get_file_content(path):
    """
    :param path:
    :return: (fileMeta, htmlContent or None)
    """
    mdfilepath = path
    if os.path.isdir(mdfilepath):
        # target is a direcoty, try get its `index.md`
        index_file = os.path.join(path, _INDEX_FILE)
        if os.path.exists(index_file):
            mdfilepath = index_file
        else:
            mdfilepath = None

    # only accept markdown file
    if mdfilepath is None or not mdfilepath.endswith('.md'):
        meta = {
            _MARKDOWN_TITLE: os.path.split(path)[-1]
        }
        content = None
    else:
        with open(mdfilepath, 'r') as f:
            data = f.read()
            meta, content = _markdown_parse(data)
            meta[_MARKDOWN_TITLE] = meta.get(_MARKDOWN_TITLE, os.path.split(path)[-1][:-3])

    return meta, content


def get_blog(path):
    """
    get title and html content of file
    :param path: path to your file system
    :return: (title, html)
    """
    realpath = os.path.join(CONFIG.BASE_FOLDER, path)
    meta, content = get_file_content(realpath)
    return meta[_MARKDOWN_TITLE], content


def _create_menu(path, base_folder):
    is_folder = os.path.isdir(path)

    meta, _htmlcontent = get_file_content(path)

    relative_path = path[len(base_folder):]
    return Menu(meta[_MARKDOWN_TITLE], relative_path, is_folder)


def get_menus():
    """
    Show packages and files your repository have.
    :return: list of Menu
    """
    base_folder = CONFIG.BASE_FOLDER

    def search_folder(path):
        menus = []
        for f in os.listdir(path):
            # index.md is a special file for folder,
            # no need to show in menu.
            if f == _INDEX_FILE:
                continue

            _fullpath = os.path.join(path, f)
            m = _create_menu(_fullpath, base_folder)
            if m.is_folder:
                m.children = search_folder(_fullpath)

            menus.append(m)

        menus = sorted(menus, key=lambda x: x.title)
        return menus

    return search_folder(base_folder)

