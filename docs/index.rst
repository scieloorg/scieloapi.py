.. scieloapi.py documentation master file, created by
   sphinx-quickstart on Fri Aug  2 10:49:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

scieloapi.py
============

Release v\ |version|.
This software is licensed under `BSD License <http://opensource.org/licenses/BSD-2-Clause>`_.

Usage example::

    >>> import scieloapi

    >>> client = scieloapi.Client('some.user', 'some.api_key')
    
    >>> for journal in client.query('journals').all():
    ...    print journal['id'], journal['title']


User guide
----------

Step-by-step guide to use the features provided by scieloapi.py for
exploring data from SciELO. 

.. toctree::
   :maxdepth: 2

   narr/install
   narr/quickstart


API documentation
-----------------

If you are looking for information about the library internals,
this if for you.

.. toctree::
   :maxdepth: 2

   api

