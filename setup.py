#!/usr/bin/env python

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'Readme.md')).read()

requires = [
    'django',
    'https://github.com/hanlucen/sms-provider-python/archive/master.zip'
]

includes = (
    'sms',
)

setup(
    name="sms-client-python",
    version='0.0.1',
    packages=find_packages(),
    install_requires=requires,
    description='a python client for sms',
    long_description=README,
    author="zhumengyuan",
    license="BSD",
    url=""
)
