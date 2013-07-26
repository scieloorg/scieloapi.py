#!/usr/bin/env python
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


setup(
    name="scieloapi",
    version='0.2',
    description="Thin wrapper around the SciELO Manager RESTful API.",
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.md').read(),
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license=open('LICENSE').read(),
    url="http://docs.scielo.org",
    packages=['scieloapi'],
    package_data={'': ['README.md', 'HISTORY.md', 'LICENSE']},
    package_dir={'scieloapi': 'scieloapi'},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=["mocker"],
    test_suite='tests',
    install_requires=['requests'],
)

