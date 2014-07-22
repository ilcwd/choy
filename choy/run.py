# coding:utf8
"""

Author: ilcwd
"""
import sys
reload(sys).setdefaultencoding('utf8')

from choy.init import application, CONFIG

# import module views to initialize view functions
# noinspection PyUnresolvedReferences
import choy.views


def main():

    host, port = '0.0.0.0', 8080
    print "[INFO]Loading markdown files from:", CONFIG.BASE_FOLDER
    application.run(host, port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
