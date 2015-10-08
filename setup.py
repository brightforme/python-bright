# coding=utf-8
import os

from setuptools import find_packages
from setuptools import setup

import bright

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = "python-bright",
    version = bright.__version__,
    description = bright.__descr__,
    long_description = long_description,
    author = bright.__author__,
    author_email = bright.__author_mail__,
    license = "MIT License",
    url = bright.__url__,
    keywords = bright.__keywords__,
    classifiers = bright.__classifiers__,
    packages = find_packages(),
    include_package_data = True,
    install_requires=['requests>=2.7.0', 
                      'oauthlib',
                      'requests-oauthlib>=0.5.0'],
    zip_safe = False
)
