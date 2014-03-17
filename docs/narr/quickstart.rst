.. _quickstart:

Quickstart
==========

When a `scieloapi.Client` instance is initialized, the process automaticaly 
instrospects the API server in order to make available only the endpoints part 
of the specified API version. The API version may be passed as keyword argument 
`version` when creating the `scieloapi.Client` instance. If ommited, the highest 
version is used.

::

    >>> client = scieloapi.Client('some.user', 'some.api_key') 
    

Listing available endpoints::

    >>> client.endpoints
    [u'pressreleases', u'users', u'sections', u'sponsors', u'collections', u'changes', u'apressreleases', u'uselicenses', u'journals', u'issues']
    >>>

Listing all items of an endpoint::

    >>> for journal in client.query('journals').all(): print journal['title']
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


Listing items matching some params::

    >>> for journal in client.query('journals').filter(collection='saude-publica'): print journal['title']
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


Getting a specific item::

    >>> journal = client.query('journals').get(62)
    >>> journal['title']
    u'Acta M\xe9dica Costarricense'
    >>>

