#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


setup(
    name="scieloapi",
    version='0.1',
    description="Thin wrapper around the SciELO Manager RESTful API.",
    author="Gustavo Fonseca",
    author_email="gustavofons@gmail.com",
    license="BSD",
    url="http://docs.scielo.org",
    py_modules=["scieloapi"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=["mocker"],
    test_suite='tests',
)
