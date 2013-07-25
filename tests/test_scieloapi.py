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

    def test_fetching_all_docs_of_an_endpoint(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={'username': 'any.username', 'api_key': 'any.apikey'},
                            resource_id=None)
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey')

        with doubles.Patch(conn, '_httpbroker', mock_httpbroker):
            res = conn.fetch_data('journals')
            self.assertTrue('objects' in res)
            self.assertTrue(len(res['objects']), 1)

    def test_single_document_of_an_endpoint(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={'username': 'any.username', 'api_key': 'any.apikey'},
                            resource_id=1)
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey')

        with doubles.Patch(conn, '_httpbroker', mock_httpbroker):
            res = conn.fetch_data('journals', resource_id=1)
            self.assertIn('title', res)

    def test_fetch_data_with_querystring_params(self):
        mock_httpbroker = self.mocker.mock()

        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={
                                'username': 'any.username',
                                'api_key': 'any.apikey',
                                'collection': 'saude-publica',
                            },
                            resource_id=1)
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey')

        with doubles.Patch(conn, '_httpbroker', mock_httpbroker):
            res = conn.fetch_data('journals', resource_id=1, collection='saude-publica')
            self.assertIn('title', res)

    def test_unsupported_api_version_raises_ValueError(self):
        self.assertRaises(ValueError,
            lambda: self._makeOne('any.username',
                                  'any.apikey',
                                  version='vFoo'))

    def test_unsupported_api_version_at_API_VERSIONS_raises_RequestError(self):
        import requests
        mock_httpbroker = self.mocker.mock()
        mock_httpbroker.get('http://manager.scielo.org/api/v1/',
                            endpoint='journals',
                            params={
                                'username': 'any.username',
                                'api_key': 'any.apikey',
                            },
                            resource_id=None)
        self.mocker.throw(requests.exceptions.HTTPError)
        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey')

        with doubles.Patch(conn, '_httpbroker', mock_httpbroker):
            self.assertRaises(exceptions.RequestError,
                              lambda: conn.fetch_data('journals'))

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

    @unittest.skip('')
    def test_connector_instance_created_during_initialization(self):
        pass

    @unittest.skip('')
    def test_endpoints_introspected_during_initialization(self):
        pass

    @unittest.skip('')
    def test_missing_attributes_are_handled_as_endpoints(self):
        pass

    @unittest.skip('')
    def test_unknown_missing_attribute_raises_AttributeError(self):
        pass

    @unittest.skip('')
    def test_username_and_apikey_are_mandatory_during_initialization(self):
        pass

    @unittest.skip('')
    def test_api_uri_parameterized_during_initialization(self):
        pass

    @unittest.skip('')
    def test_api_uri_defaults_to_manager_scielo_org(self):
        pass

    @unittest.skip('')
    def test_version_parameterized_during_initialization(self):
        pass

    @unittest.skip('')
    def test_version_restricted_to_API_VERSIONS(self):
        pass

    @unittest.skip('')
    def test_missing_version_defaults_to_newest(self):
        pass

    @unittest.skip('')
    def test_invalid_credentials_raises_Unauthorized(self):
        """
        See https://github.com/scieloorg/scieloapi.py/issues/1
        """
        pass

