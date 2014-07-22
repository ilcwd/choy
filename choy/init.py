# coding:utf8
"""

Author: ilcwd
"""
import os
import logging

import flask


class CONFIG(object):
    """
    Global config.
    """
    # get your markdown repository from env
    BASE_FOLDER = os.getenv("CHOY_HOME") or '.'

    # template folder is your templates for rendering,
    # MUST include file named `base.html`, the template it read;
    # Can include folder named `static`, if your want to serve static files.
    TEMPLATE_FOLDER = os.getenv("CHOY_TEMPLATE") or 'templates/default'


# Flask application
application = flask.Flask(
    __name__,
    static_folder=os.path.join(CONFIG.TEMPLATE_FOLDER, 'static'),
    static_url_path='/static',
    template_folder=CONFIG.TEMPLATE_FOLDER,
)

# global logger, if needed
logger = logging.getLogger(__name__)