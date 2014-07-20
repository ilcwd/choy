# coding:utf8
"""
Created on Jun 18, 2014

@author: ilcwd
"""

import os
from setuptools import setup, find_packages


_CWD = os.path.dirname(__file__)

NAME = 'markdown-blog'
DESCRIPTION = 'Blog system using Markdown.'
AUTHOR = 'ilcwd'
EMAIL = 'ilcwd23@gmail.com'
INSTALL_REQUIRES = [i for i in open(os.path.join(_CWD, 'requirements.txt')).readlines()
                    if not i.startswith(('-', '#', '\n'))]
VERSION = open(os.path.join(_CWD, 'VERSION')).read().strip()

setup(
    name=NAME,
    description=DESCRIPTION,
    # long_description=open(os.path.join(_CWD, 'README.md')).read(),
    version=VERSION,
    packages=find_packages(exclude=['examples', 'tests']),
    install_requires=INSTALL_REQUIRES,
    author=AUTHOR,
    author_email=EMAIL,
    license="No License",
    platforms=['any'],
    url="",
    classifiers=["Intended Audience :: Developers",
                 "Programming Language :: Python",
                 "Topic :: Blog",
                 "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
