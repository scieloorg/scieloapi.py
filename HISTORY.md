History
=======

0.4 (2013-08-30)
----------------

* Params are sorted by key before the GET request is dispatched. This minor
  change aims to improve server-side caching capabilities.
* Minor changes to the API of the function `httpbroker.get`. It now accepts a `auth` kwarg
  to handle server-side authentication.
* Minor changes to `scieloapi.Connector`:
  * A custom http broker can be passed as `http_broker` kwarg during init.
  * Http methods are created dinamically during initialization, with user credentials bound 
    into it. Api_key is no longer maintained by the instance.
* `Client.fetch_relations` now accepts the param `only` to specify a subset of relations to fetch.
* Now the User-Agent is set to `scieloapi/:version`.
* The module `scieloapi.scieloapi` was renamed to `scieloapi.core` to make things clearer.
* Added POST method capabilities on endpoints.
* Added the exception `exceptions.MethodNotAllowed` to represent 405 status code.


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

