#!/usr/bin/env python

from distutils.core import setup

setup(name='moses',
    version='0.1',
    description='Splitting PDF files into chunks. ',
    author='Lennart Mühlenmeier',
    author_email='lennart@lnrt.de',
    url='https://github.com/riotbib/moses',
    py_modules=['moses'],
    entry_points={
        'console_scripts': [
            'moses = moses:moses',
        ],
    },
    )
