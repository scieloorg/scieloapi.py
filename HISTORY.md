History
=======

0.3 (2013-08-02)
----------------

* Added more unit tests (Now at 73% of code coverage).
* Minor adjusts at `setup.py` installation script.
* New exceptions to represent http status codes.
* Better documentation at `http://docs.scielo.org/projects/scieloapipy/`.


0.2 (2013-07-26)
----------------

* Slumber dependency was removed. The module `scieloapi.httpbroker` was created
  to deal with http requests and responses.
* Better test reports now using Nosetests + coverage.
* Added method `Client.fetch_relations` to fetch all first-level relations of
  a document and replace the value by the full document.

