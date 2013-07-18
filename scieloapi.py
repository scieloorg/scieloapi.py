# coding: utf-8
import logging
import time

import slumber
import requests


logger = logging.getLogger(__name__)

ITEMS_PER_REQUEST = 50
API_VERSIONS = ('v1',)


class ResourceUnavailableError(Exception):
    pass


class RequestError(Exception):
    pass


class Connector(object):
    """
    Encapsulates the HTTP requests layer.
    """
    # caches endpoints definitions
    _cache = {}

    def __init__(self,
                 username,
                 api_key,
                 api_uri=None,
                 version=None,
                 slumber_dep=slumber):
        # dependencies
        self._slumber_lib = slumber_dep

        # setup
        if not api_uri:
            self.api_uri = r'http://manager.scielo.org/api/'
        else:
            self.api_uri = api_uri

        if version :
            if version in API_VERSIONS:
                self.version = version
            else:
                raise ValueError('unsupported api version. supported are: %s' % ', '.join(API_VERSIONS))
        else:
            self.version = sorted(API_VERSIONS)[-1]

        self.username = username
        self.api_key = api_key
        self.api_uri = self.api_uri + self.version + '/'
        self._api = self._slumber_lib.API(self.api_uri)

    def fetch_data(self, endpoint,
                         resource_id=None,
                         **kwargs):
        """
        Fetches the specified resource from the SciELO Manager API.

        ``endpoint`` must be a valid endpoint at
        http://manager.scielo.org/api/v1/
        """
        err_count = 0

        if all([self.username, self.api_key]):
            kwargs['username'] = self.username
            kwargs['api_key'] = self.api_key

        resource = getattr(self._api, endpoint)

        if resource_id:
            resource = resource(resource_id)

        while True:
            try:
                return resource.get(**kwargs)
            except requests.exceptions.ConnectionError as exc:
                if err_count < 10:
                    wait_secs = err_count * 5
                    logger.info('Connection failed. Waiting %ss to retry.' % wait_secs)
                    time.sleep(wait_secs)
                    err_count += 1
                    continue
                else:
                    logger.error('Unable to connect to resource (%s).' % exc)
                    raise ResourceUnavailableError(exc)
            except slumber.exceptions.HttpClientError as exc:
                logger.error('Bad request: %s' % exc)
                raise RequestError(exc)
            else:
                err_count = 0

    def iter_docs(self, endpoint, **kwargs):
        """
        Iterates over all documents of a given endpoint and collection.

        ``endpoint`` must be a valid endpoint at
        http://manager.scielo.org/api/v1/

        ``kwargs`` are passed thru the request as query string
        params

        Note that you need a valid API KEY in order to query the
        Manager API. Read more at: http://ref.scielo.org/ddkpmx
        """
        offset = 0
        limit = ITEMS_PER_REQUEST

        qry_params = {'limit': limit}
        qry_params.update(kwargs)

        while True:
            qry_params.update({'offset': offset})
            doc = self.fetch_data(endpoint, **qry_params)

            for obj in doc['objects']:
                # we are interested only in non-trashed items.
                if obj.get('is_trashed'):
                    continue

                yield obj

            if not doc['meta']['next']:
                raise StopIteration()
            else:
                offset += ITEMS_PER_REQUEST

    def get_endpoints(self):
        """
        Get all endpoints available for the given API version.
        """
        cls = self.__class__

        if self.version not in cls._cache:
            try:
                cls._cache[self.version] = getattr(self._api, '').get()
            except slumber.exceptions.HttpClientError as exc:
                raise ResourceUnavailableError(exc)

        return cls._cache[self.version]


class Endpoint(object):
    def __init__(self, name, connector):
        self.name = name
        self.connector = connector

    def get(self, resource_id):
        res = self.connector.fetch_data(self.name, resource_id=resource_id)
        return res

    def all(self):
        return self.connector.iter_docs(self.name)

    def filter(self, **kwargs):
        return self.connector.iter_docs(self.name, **kwargs)


class Client(object):
    """
    Collection of endpoints made available in an object oriented fashion.

    An instance of Client tries to figure out the available endpoints
    for the version of the API the Client is instantiated for. If ``version``
    is missing, the default behaviour is to use the most recent version.
    """
    def __init__(self,
                 username,
                 api_key,
                 api_uri=None,
                 version=None):

        self._connector = Connector(username,
                                    api_key,
                                    api_uri=api_uri,
                                    version=version)
        self._endpoints = {}
        for ep in self._introspect_endpoints():
            self._endpoints[ep] = Endpoint(ep, self._connector)

    def _introspect_endpoints(self):
        """
        Contact the API server to discover the available endpoints.
        """
        return self._connector.get_endpoints().keys()

    def __getattr__(self, name):
        """
        Missing attributes are assumed to be endpoint lookups.
        i.e. Client.journals.all()
        """
        if name in self._endpoints:
            return self._endpoints[name]
        else:
            raise AttributeError()

    @property
    def endpoints(self):
        return self._endpoints.keys()

