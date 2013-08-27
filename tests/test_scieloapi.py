# coding: utf-8
import unittest
import mocker

from scieloapi import exceptions
import doubles


class ConnectorHttpBrokerCollaborationTests(mocker.MockerTestCase):
    valid_full_microset = {
        'objects': [
            {
                'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
            },
        ],
        'meta': {'next': None},
    }
    valid_microset = {
        'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
    }

    def _makeOne(self, *args, **kwargs):
        from scieloapi import Connector
        return Connector(*args, **kwargs)

    def test_api_uri_defaults_to_manager_scielo_org(self):
        conn = self._makeOne('any.username', 'any.apikey')
        self.assertTrue(conn.api_uri.startswith('http://manager.scielo.org'))

    def test_fetching_all_docs_of_an_endpoint(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=None,
                            auth=('any.username', 'any.apikey'))
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        res = conn.fetch_data('journals')
        self.assertTrue('objects' in res)
        self.assertTrue(len(res['objects']), 1)

    def test_single_document_of_an_endpoint(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=1,
                            auth=('any.username', 'any.apikey'))
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        res = conn.fetch_data('journals', resource_id=1)
        self.assertIn('title', res)

    def test_connection_error_fetching_data_raises_ConnectionError_after_retries(self):
        from scieloapi import exceptions
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=1,
                            auth=('any.username', 'any.apikey'))
        self.mocker.throw(exceptions.ConnectionError)
        self.mocker.count(11)
        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        with doubles.Patch(conn, '_time', doubles.TimeStub()):
            self.assertRaises(exceptions.ConnectionError,
                lambda: conn.fetch_data('journals', resource_id=1))

    def test_fetching_data_retry_on_ConnectionError(self):
        from scieloapi.exceptions import ConnectionError
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=1,
                            auth=('any.username', 'any.apikey'))
        self.mocker.throw(ConnectionError)

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=1,
                            auth=('any.username', 'any.apikey'))
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        res = conn.fetch_data('journals', resource_id=1)
        self.assertIn('title', res)

    def test_fetch_data_with_querystring_params(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={
                                'collection': 'saude-publica',
                            },
                            resource_id=1,
                            auth=('any.username', 'any.apikey'))
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        res = conn.fetch_data('journals', resource_id=1, collection='saude-publica')
        self.assertIn('title', res)

    def test_unsupported_api_version_raises_ValueError(self):
        self.assertRaises(ValueError,
            lambda: self._makeOne('any.username',
                                  'any.apikey',
                                  version='vFoo'))

    def test_unsupported_api_version_at_API_VERSIONS_raises_NotFound(self):
        import scieloapi
        mock_httpbroker = self.mocker.mock()
        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={},
                            resource_id=None,
                            auth=('any.username', 'any.apikey'))
        self.mocker.throw(scieloapi.exceptions.NotFound)
        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', http_broker=mock_httpbroker)

        self.assertRaises(scieloapi.exceptions.NotFound,
                          lambda: conn.fetch_data('journals'))

    def test_known_version_can_be_used(self):
        """
        This test needs to change a module level variable, so
        it needs to be restored to avoid side effects on other
        tests.
        """
        from scieloapi import scieloapi
        old_api_versions = scieloapi.API_VERSIONS

        scieloapi.API_VERSIONS += ('v2',)

        conn = scieloapi.Connector('any.user', 'any.apikey', version='v2')
        self.assertEqual(conn.version, 'v2')

        scieloapi.API_VERSIONS = old_api_versions

    def test_iteration_over_endpoint_items(self):
        def fetch_data_stub(self, *args, **kwargs):
            return self.valid_full_microset

        conn = self._makeOne('any.username', 'any.apikey')
        with doubles.Patch(conn, 'fetch_data', fetch_data_stub, instance_method=True):
            res = conn.iter_docs('journals')

class EndpointTests(mocker.MockerTestCase):
    valid_microset = {
        'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
    }

    def _makeOne(self, *args, **kwargs):
        from scieloapi import Endpoint
        return Endpoint(*args, **kwargs)

    def test_get_valid_resource(self):
        mock_connector = self.mocker.mock()
        mock_connector.fetch_data('journals', resource_id=1)
        self.mocker.result(self.valid_microset)
        self.mocker.replay()

        journal_ep = self._makeOne('journals', mock_connector)
        self.assertEqual(journal_ep.get(1), self.valid_microset)


class ClientTests(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from scieloapi import Client
        return Client(*args, **kwargs)

    def test_connector_instance_created_during_initialization(self):
        mock_connector = self.mocker.mock()
        mock_connector('any.user', 'any.apikey', api_uri=None, version=None)
        self.mocker.result(mock_connector)
        mock_connector.get_endpoints()
        self.mocker.result({'journals': None})
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey', connector_dep=mock_connector)

    def test_endpoints_introspected_during_initialization(self):
        mock_connector = self.mocker.mock()
        mock_connector('any.user', 'any.apikey', api_uri=None, version=None)
        self.mocker.result(mock_connector)
        mock_connector.get_endpoints()
        self.mocker.result({'journals': None})
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey', connector_dep=mock_connector)
        self.assertEqual(client.endpoints, ['journals'])

    def test_missing_attributes_are_handled_as_endpoints(self):
        mock_endpoints = self.mocker.mock()
        'journals' in mock_endpoints
        self.mocker.result(True)
        mock_endpoints['journals']
        self.mocker.result('foo')
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey', connector_dep=doubles.ConnectorStub)
        with doubles.Patch(client, '_endpoints', mock_endpoints):
            j = client.journals
            self.assertEqual(j, 'foo')

    def test_unknown_missing_attribute_raises_AttributeError(self):
        mock_endpoints = self.mocker.mock()
        'journals' in mock_endpoints
        self.mocker.result(False)
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey', connector_dep=doubles.ConnectorStub)
        with doubles.Patch(client, '_endpoints', mock_endpoints):
            self.assertRaises(AttributeError, lambda: client.journals)

    def test_username_and_username_are_mandatory_during_initialization(self):
        self.assertRaises(TypeError, lambda: self._makeOne('any.user'))

    def test_api_uri_parameterized_during_initialization(self):
        mock_connector = self.mocker.mock()
        mock_connector('any.user', 'any.apikey', api_uri='http://foo.org/api/', version=None)
        self.mocker.result(mock_connector)
        mock_connector.get_endpoints()
        self.mocker.result({'journals': None})
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey',
            api_uri='http://foo.org/api/', connector_dep=mock_connector)

    def test_version_parameterized_during_initialization(self):
        mock_connector = self.mocker.mock()
        mock_connector('any.user', 'any.apikey', api_uri=None, version='vFoo')
        self.mocker.result(mock_connector)
        mock_connector.get_endpoints()
        self.mocker.result({'journals': None})
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey',
            version='vFoo', connector_dep=mock_connector)

    def test_version_restricted_to_API_VERSIONS(self):
        self.assertRaises(
            ValueError,
            lambda: self._makeOne('any.user', 'any.apikey', version='vFoo'))

    def test_missing_version_defaults_to_newest(self):
        from scieloapi.scieloapi import API_VERSIONS
        newest = sorted(API_VERSIONS)[-1]

        client = self._makeOne('any.user', 'any.apikey')
        self.assertEqual(client.version, newest)

    def test_known_version_can_be_used(self):
        from scieloapi.scieloapi import API_VERSIONS
        API_VERSIONS += ('v2',)

        mock_connector = self.mocker.mock()
        mock_connector('any.user', 'any.apikey', api_uri=None, version='v2')
        self.mocker.result(mock_connector)
        mock_connector.get_endpoints()
        self.mocker.result({'journals': None})
        self.mocker.replay()

        client = self._makeOne('any.user', 'any.apikey',
            version='v2', connector_dep=mock_connector)

    @unittest.skip('')
    def test_invalid_credentials_raises_Unauthorized(self):
        """
        See https://github.com/scieloorg/scieloapi.py/issues/1
        """
        pass

    def test_fetch_relations_for_one_relation(self):
        stub_connector = doubles.ConnectorStub
        mock_get = self.mocker.mock()
        mock_get(mocker.ANY, '/api/v1/journals/70/')
        self.mocker.result({'title': 'foo'})
        self.mocker.replay()

        data = {'journal': '/api/v1/journals/70/'}

        client = self._makeOne('any.user', 'any.apikey', connector_dep=stub_connector)
        with doubles.Patch(client, 'get', mock_get, instance_method=True):
            self.assertEqual(client.fetch_relations(data), {'journal': {'title': 'foo'}})

    def test_fetch_relations_for_all_relations(self):
        stub_connector = doubles.ConnectorStub
        mock_get = self.mocker.mock()
        mock_get(mocker.ANY, '/api/v1/journals/70/')
        self.mocker.result({'title': 'foo'})
        mock_get(mocker.ANY, '/api/v1/issues/71/')
        self.mocker.result({'title': 'bar'})
        self.mocker.replay()

        data = {'journal': '/api/v1/journals/70/',
                'issue': '/api/v1/issues/71/'}

        client = self._makeOne('any.user', 'any.apikey', connector_dep=stub_connector)
        with doubles.Patch(client, 'get', mock_get, instance_method=True):
            self.assertEqual(
                client.fetch_relations(data),
                {'journal': {'title': 'foo'}, 'issue': {'title': 'bar'}})

    def test_fetch_relations_for_lists(self):
        stub_connector = doubles.ConnectorStub
        mock_get = self.mocker.mock()
        mock_get(mocker.ANY, '/api/v1/journals/70/')
        self.mocker.result({'title': 'foo'})
        mock_get(mocker.ANY, '/api/v1/journals/71/')
        self.mocker.result({'title': 'bar'})
        self.mocker.replay()

        data = {'journal': ['/api/v1/journals/70/',
                            '/api/v1/journals/71/']}

        client = self._makeOne('any.user', 'any.apikey', connector_dep=stub_connector)
        with doubles.Patch(client, 'get', mock_get, instance_method=True):
            self.assertEqual(
                client.fetch_relations(data),
                {'journal': [{'title': 'foo'}, {'title': 'bar'}]})

    def test_fetch_relations_for_specific_relations(self):
        stub_connector = doubles.ConnectorStub
        mock_get = self.mocker.mock()
        mock_get(mocker.ANY, '/api/v1/journals/70/')
        self.mocker.result({'title': 'foo'})
        self.mocker.replay()

        data = {'journal': '/api/v1/journals/70/',
                'issue': '/api/v1/issues/71/'}

        client = self._makeOne('any.user', 'any.apikey', connector_dep=stub_connector)
        with doubles.Patch(client, 'get', mock_get, instance_method=True):
            self.assertEqual(
                client.fetch_relations(data, only=('journal',)),
                {'journal': {'title': 'foo'}, 'issue': '/api/v1/issues/71/'})

