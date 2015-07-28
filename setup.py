# coding=utf-8
import os

from setuptools import find_packages
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name = "python-bright",
    version = "0.0.1",
    description = "BRIGHT API wrapper",
    long_description = long_description,
    author = "Martin-Zack Mekkaoui",
    author_email = "martin@brightfor.me",
    license = "MIT License",
    url = "https://github.com/bright/python-bright/",
    keywords = 'bright digital art',
    classifiers = [],
    packages = find_packages(),
    include_package_data = True,
    install_requires=['requests', 'requests-oauthlib'],
    zip_safe = False
)