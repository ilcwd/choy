#coding:utf8
"""
Created on Jun 18, 2014

@author: ilcwd
"""

from openauth import application


import logging.config
import os
logging_config_path = os.path.join(os.path.dirname(__file__), 'openauth.logging.conf')
logging.config.fileConfig(logging_config_path)


def main():
    """Debug Mode"""
    host, port = '0.0.0.0', 8080
    print 'Run on', host, port
    application.run(host, port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()