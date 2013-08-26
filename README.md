scieloapi.py
============

Thin wrapper around the SciELO Manager RESTful API.

[![Build Status](https://travis-ci.org/scieloorg/scieloapi.py.png?branch=master)](https://travis-ci.org/scieloorg/scieloapi.py)

Usage example:

    import scieloapi

    client = scieloapi.Client('some.user', 'some.api_key')
    
    for journal in client.journals.all():
        print journal['id'], journal['title']


How to install
--------------

You can install it via `pip`, directly from the github repo:

    pip install -e git+git://github.com/scieloorg/scieloapi.py.git#egg=scieloapi

Or from PyPi (more stable):

    pip install scieloapi


Basics
------

When a `Client` instance is initialized, the process automaticaly instrospects the API server
in order to make available only the endpoints part of the specified API version. The API version
may be passed as keyword argument `version` when creating the `Client` instance. If ommited, 
the highest version is used.


    >>> client = scieloapi.Client('some.user', 'some.api_key', api_uri='http://manager.scielo.org/api/', version='v1')
    

Listing available endpoints:

    >>> client.endpoints
    [u'pressreleases', u'users', u'sections', u'sponsors', u'collections', u'changes', u'apressreleases', u'uselicenses', u'journals', u'issues']
    >>>

Listing all items of an endpoint:

    >>> for journal in client.journals.all(): print journal['title']
    ...
    Acta Médica Costarricense
    Acta Pediátrica Costarricense
    Actualidades Investigativas en Educación
    Adolescencia y Salud
    Agronomía Costarricense
    Agronomía Mesoamericana
    Annali dell'Istituto Superiore di Sanità
    Arquivos em Odontologia
    Brazilian Journal of Oral Sciences
    Bulletin of the World Health Organization
    Cadernos de Saúde Pública
    >>> 


Listing items matching some params:

    >>> for journal in client.journals.filter(collection='saude-publica'): print journal['title']
    ...
    Annali dell'Istituto Superiore di Sanità
    Bulletin of the World Health Organization
    Cadernos de Saúde Pública
    Ciência & Saúde Coletiva
    Gaceta Sanitaria
    MEDICC Review
    Revista Brasileira de Epidemiologia
    Revista Cubana de Salud Pública
    Revista de Salud Pública
    >>>


Getting a specific item:

    >>> journal = client.journals.get(62)
    >>> journal['title']
    u'Acta M\xe9dica Costarricense'
    >>>


Use license
-----------

This project is licensed under FreeBSD 2-clause. See `LICENSE` for more details.
