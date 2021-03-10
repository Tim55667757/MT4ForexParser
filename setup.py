# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with Travis CI


from setuptools import setup
import os

__version__ = "1.1"

devStatus = "4 - Beta"

if "TRAVIS_BUILD_NUMBER" in os.environ and "TRAVIS_BRANCH" in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ["TRAVIS_BUILD_NUMBER"]))
    print("TRAVIS_BRANCH = {}".format(os.environ["TRAVIS_BRANCH"]))

    __version__ += ".{}{}".format(
        "" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else "dev",
        os.environ["TRAVIS_BUILD_NUMBER"],
    )

    devStatus = "5 - Production/Stable" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else devStatus

else:
    print("This is local build")
    __version__ += ".dev0"  # set version as major.minor.localbuild if local build: python setup.py install

print("MT4ForexParser build version = {}".format(__version__))

setup(
    name="mt4forexparser",

    version=__version__,

    description="Read forex data in MetaTrader 4 .hst-format and convert into .csv file and pandas dataframe. Also you can draw an interactive chart.",

    long_description="GitHub Pages: https://tim55667757.github.io/MT4ForexParser",

    license="MIT",

    author="Timur Gilmullin",

    author_email="tim55667757@gmail.com",

    url="https://github.com/Tim55667757/MT4ForexParser/",

    download_url="https://github.com/Tim55667757/MT4ForexParser.git",

    entry_points={"console_scripts": ["mt4forexparser = mt4forexparser.MT4ForexParser:Main"]},

    classifiers=[
        "Development Status :: {}".format(devStatus),
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],

    keywords=[
        "forex",
        "broker",
        "history",
        "csv",
        "stock",
        "trade",
        "candlestick",
        "chart",
        "parser",
        "MetaTrader",
        "MetaTrader4",
    ],

    tests_require=[
        "pytest>=6.2.2",
        "pandas>=1.2.2",
        "pricegenerator>=1.2.46",
    ],

    install_requires=[
        "pandas>=1.2.2",
        "pricegenerator>=1.2.46",
    ],

    packages=[
        "mt4forexparser",
    ],

    zip_safe=True,
)
