# coding:utf8
"""

Author: ilcwd
"""

import flask
import logging

application = flask.Flask(
    __name__,
    static_folder='static',
)

logger = logging.getLogger(__name__)

config = {
    'base_folder': '/home/ilcwd/Documents/markdown',
}