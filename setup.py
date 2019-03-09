# -*- coding: utf-8 -*-
from os.path import join, dirname

from setuptools import setup, find_packages

import helloworld


setup(
    name='helloworld',
    version=helloworld.__version__,
    packages=find_packages(),
    description='Sample',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    url='http://github.com/alvadia/Python_Project_2019',
    license='MIT',
    install_requires=[
    ],
    extras_require={
        'dev': [],
        'build': []
    },
    entry_points={
        'console_scripts': [
            'helloworld = helloworld.core:print_message',
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    test_suite='tests'
)
