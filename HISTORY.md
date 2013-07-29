History
=======

0.3
---

* Added more unit tests (Now at 73% of code coverage).
* Minor adjusts at `setup.py` installation script.


0.2 (2013-07-26)
----------------

* Slumber dependency was removed. The module `scieloapi.httpbroker` was created
  to deal with http requests and responses.
* Better test reports now using Nosetests + coverage.
* Added method `Client.fetch_relations` to fetch all first-level relations of
  a document and replace the value by the full document.

