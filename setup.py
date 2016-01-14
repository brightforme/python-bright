# coding=utf-8
import os

from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = "python-bright",
    version = "0.0.8",
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
    install_requires=['requests>=2.7.0', 
                      'oauthlib',
                      'requests-oauthlib==0.5.0'],
    zip_safe = False
)
