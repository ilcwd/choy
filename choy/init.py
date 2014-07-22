# coding:utf8
"""

Author: ilcwd
"""
import os
import logging
import optparse

import flask

_current = os.path.dirname(os.path.realpath(__file__))


parser = optparse.OptionParser()
parser.add_option('-f', '--folder', dest='BASE_FOLDER',
                  default=os.getcwd(),
                  help="markdown repository")
parser.add_option('-T', '--template', dest='TEMPLATE_FOLDER',
                  default=os.path.join(_current, 'templates', 'default'),
                  help="template folder")
parser.add_option('-l', '--host', dest='HOST',
                  default='0.0.0.0', type='string',
                  help="listening host")
parser.add_option('-p', '--port', dest='PORT',
                  default=8080, type='int',
                  help="listening port")
(options, args) = parser.parse_args()


CONFIG = options
# class CONFIG(object):
#     """
#     Global config.
#     """
#     # get your markdown repository from env
#     BASE_FOLDER = options.BASE_FOLDER
#
#     # template folder is your templates for rendering,
#     # MUST include file named `base.html`, the template it read;
#     # Can include folder named `static`, if your want to serve static files.
#     TEMPLATE_FOLDER = options.TEMPLATE_FOLDER
#
#     PORT = options.PORT


# Flask application
application = flask.Flask(
    __name__,
    static_folder=os.path.join(CONFIG.TEMPLATE_FOLDER, 'static'),
    static_url_path='/static',
    template_folder=CONFIG.TEMPLATE_FOLDER,
)

# global logger, if needed
logger = logging.getLogger(__name__)