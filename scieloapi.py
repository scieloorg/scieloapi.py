# coding: utf-8
import logging
import time

import slumber
import requests


logger = logging.getLogger(__name__)

ITEMS_PER_REQUEST = 50
API_VERSIONS = ('v1',)


class ResourceUnavailableError(Exception):
    def __init__(self, *args, **kwargs):
        super(ResourceUnavailableError, self).__init__(*args, **kwargs)


class Connector(object):
    """
    Encapsulates the HTTP requests layer.
    """
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

        if version and version in API_VERSIONS:
            self.version = version
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

        self.journals = Endpoint('journals', self._connector)
        self.issues = Endpoint('issues', self._connector)
        self.changes = Endpoint('changes', self._connector)
        self.collections = Endpoint('collections', self._connector)
        self.apressreleases = Endpoint('apressreleases', self._connector)
        self.pressreleases = Endpoint('pressreleases', self._connector)
        self.sections = Endpoint('sections', self._connector)
        self.sponsors = Endpoint('sponsors', self._connector)
        self.uselicenses = Endpoint('uselicenses', self._connector)
        self.users = Endpoint('users', self._connector)

