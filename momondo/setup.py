#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='6883',

    version='1.0.0',

    description='Crawld hotel information from momondo.com',

    url='https://github.com/germangh/spiders',

    author='German Gomez-Herrero',
    author_email='german@innovativetravel.eu',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],

    packages=find_packages(),

    install_requires=['scrapy']

)
