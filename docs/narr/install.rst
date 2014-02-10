.. _install:

Installation
============

This part of the documentation covers the installation process of scieloapi.py.


Pip
---

Installing scieloapi.py is simple with `pip <http://www.pip-installer.org/>`_::

   $ pip install scieloapi


Get the Code
------------

scieloapi.py is actively developed on GitHub, check it out 
`here <https://github.com/scieloorg/scieloapi.py>`_.

You can either clone the public repository::

    git clone git://github.com/scieloorg/scieloapi.py.git

Download the `tarball <https://github.com/scieloorg/scieloapi.py/tarball/master>`_::

    $ curl -OL https://github.com/scieloorg/scieloapi.py/tarball/master

Or, download the `zipball <https://github.com/scieloorg/scieloapi.py/zipball/master>`_::

    $ curl -OL https://github.com/scieloorg/scieloapi.py/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install


Settings up the logger handler
==============================

It is expected that the application using `scieloapi` defines a logger for `scieloapi`, e.g.::

    logging.getLogger('scieloapi').addHandler(logging.StreamHandler())

See the official `docs <http://docs.python.org/2.7/howto/logging.html#configuring-logging>`_ for more info.

