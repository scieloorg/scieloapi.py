# coding: utf-8
import re
import logging
import time

import requests #leak, httpbroker must isolate requests lib

import httpbroker
import exceptions


logger = logging.getLogger(__name__)

ITEMS_PER_REQUEST = 50
API_VERSIONS = ('v1',)


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
                 version=None):
        # dependencies
        self._httpbroker = httpbroker

        # setup
        self.api_uri = api_uri if api_uri else r'http://manager.scielo.org/api/'

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

    def fetch_data(self, endpoint,
                         resource_id=None,
                         **kwargs):
        """
        Fetches the specified resource from the SciELO Manager API.

        ``endpoint`` must be a valid endpoint at
        http://manager.scielo.org/api/v1/
        """
        err_count = 0

        if self.username and self.api_key:
            kwargs['username'] = self.username
            kwargs['api_key'] = self.api_key

        while True:
            try:
                return self._httpbroker.get(self.api_uri,
                                            endpoint=endpoint,
                                            resource_id=resource_id,
                                            params=kwargs)

            except requests.exceptions.ConnectionError as exc:
                if err_count < 10:
                    wait_secs = err_count * 5
                    logger.info('Connection failed. Waiting %ss to retry.' % wait_secs)
                    time.sleep(wait_secs)
                    err_count += 1
                    continue
                else:
                    logger.error('Unable to connect to resource (%s).' % exc)
                    raise exceptions.ResourceUnavailableError(exc)
            except requests.exceptions.HTTPError as exc:
                logger.error('Bad request: %s' % exc)
                raise exceptions.RequestError(exc)
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
                cls._cache[self.version] = self._httpbroker.get(self.api_uri)
            except requests.exceptions.HTTPError as exc:
                raise exceptions.ResourceUnavailableError(exc)

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
                 version=None,
                 connector_dep=Connector):

        self._connector = connector_dep(username,
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
        """
        Lists all available endpoints for the api version
        the Client was created to interact.
        """
        return self._endpoints.keys()

    @property
    def version(self):
        """
        The API version the Client instance is interfacing with.
        """
        return self._connector.version

    def fetch_relations(self, dataset):
        """
        Returns a new dataset with all relations to
        resources changed by the actual resource data.
        """
        new_dataset = {}

        for attr_name, attr_value in dataset.items():
            # skip fetching itself
            if attr_name == 'resource_uri':
                new_dataset[attr_name] = attr_value
            elif isinstance(attr_value, basestring):
                try:
                    new_dataset[attr_name] = self.get(attr_value)
                except ValueError as e:
                    new_dataset[attr_name] = attr_value

            elif isinstance(attr_value, list):
                new_elems = []
                for elem in attr_value:
                    try:
                        new_elems.append(self.get(elem))
                    except (TypeError, ValueError) as e:
                        new_elems.append(elem)

                new_dataset[attr_name] = new_elems
            else:
                new_dataset[attr_name] = attr_value

        return new_dataset

    def get(self, resource_uri):
        """
        Gets data for resource_uri.

        `resource_uri` is a text string in the form
        "/api/<version>/<endpoint>/<resource_id>/". The <version>
        must match with Client's or a ValueError will be raised.
        The same goes to unknown endpoints and invalid `resource_uris`.
        """
        uri_pattern = re.compile(r'/api/(\w+)/(\w+)/(\d+)/')
        match = uri_pattern.match(resource_uri)
        if match:
            match_group = match.groups()
            try:
                return getattr(self, match_group[1]).get(match_group[2])
            except AttributeError:
                # AttributeError is raised if getattr fails to lookup the endpoint
                raise ValueError('Unknown endpoint %s' % match_group[1])
        else:
            raise ValueError('Invalid resource_uri')

