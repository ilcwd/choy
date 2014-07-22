# coding:utf8
"""

Author: ilcwd
"""

import os

import flask

from choy import misc
from choy.init import CONFIG


_INDEX_FILE = 'index.md'
_MARKDOWN_TITLE = misc.MARKDOWN_TITLE


_PARSER_REGISTER = {
    '.md': misc.markdown_parse,
    '.html': misc.html_parse,
}


class Menu(object):
    def __init__(self, title, url, is_folder=False):
        self.title = title
        self.url = url
        self.is_folder = is_folder
        self.children = []


class File(object):
    def __init__(self, path):
        self.path = path
        self.parent, self.name = os.path.split(path)
        self.is_folder = os.path.isdir(path)
        self.basename, self.ext = os.path.splitext(self.name)


def _is_supported_path(path):
    """
    check if we can show this file.
    :param path:
    :return:
    """
    parent, filename = os.path.split(path)

    if filename.startswith('.'):
        return False

    if os.path.isfile(path):
        ext = os.path.splitext(filename)[-1].lower()
        if ext not in _PARSER_REGISTER:
            return False

    return True


def parse_source(content, filename):
    """
    Parse content base on type.

    :param content:.lower()
    :param filename:
    :return:
        (meta, html) - if success, meta is a dict contains "title"
        ({}, None) - if fail to parse or not supported content.
    """

    ext = os.path.splitext(filename)[-1].lower()
    parser = _PARSER_REGISTER.get(ext)
    if not parser:
        return {}, None

    return parser(content)


def _error_page(title, msg):
    meta = {
        _MARKDOWN_TITLE: title
    }
    content = u"""
        <h1>%s</h1>
        <p>%s<p>
    """ % (flask.escape(title), flask.escape(msg))
    return meta, content


def get_file_content(path):
    """
    :param path:
    :return:
        (fileMeta, htmlContent) if success
        (None, Content) if fail
    """
    if not os.path.exists(path):
        return _error_page('404 Not Found', "We can't find the page your're looking for.")

    if not _is_supported_path(path):
        return _error_page('415 Unsupported Media Type', "The page you request is not supported.")

    mdfilepath = path
    if os.path.isdir(mdfilepath):
        # target is a direcoty, try get its `index.md`
        index_file = os.path.join(path, _INDEX_FILE)
        if os.path.exists(index_file):
            mdfilepath = index_file
        else:
            title = os.path.split(path)[-1]
            return _error_page(title, '')

    filename = os.path.split(mdfilepath)[-1]
    with open(mdfilepath, 'r') as f:
        data = f.read()

    meta, content = parse_source(data, filename)
    basename = os.path.splitext(os.path.split(path)[1])[0]
    meta[_MARKDOWN_TITLE] = meta.get(_MARKDOWN_TITLE) or basename

    return meta, content


def get_article(path):
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

            # filter unsupported type
            if not _is_supported_path(_fullpath):
                continue

            m = _create_menu(_fullpath, base_folder)
            if m.is_folder:
                m.children = search_folder(_fullpath)

            menus.append(m)

        menus = sorted(menus, key=lambda x: x.title)
        return menus

    return search_folder(base_folder)

