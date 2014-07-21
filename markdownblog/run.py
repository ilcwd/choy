# coding:utf8
"""

Author: ilcwd
"""
import sys
reload(sys).setdefaultencoding('utf8')

from markdownblog.init import application

# import module views to initialize view functions
# noinspection PyUnresolvedReferences
import markdownblog.views

def main():
    host, port = '0.0.0.0', 8080
    application.run(host, port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
