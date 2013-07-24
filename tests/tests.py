# coding: utf-8
import unittest
import mocker

from scieloapi import exceptions


class ConnectorSlumberCollaborationTests(mocker.MockerTestCase):
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
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', slumber_dep=mock_slumber)

        res = conn.fetch_data('journals')
        self.assertTrue('objects' in res)
        self.assertTrue(len(res['objects']), 1)

    def test_single_document_of_an_endpoint(self):
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber(1)
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', slumber_dep=mock_slumber)

        res = conn.fetch_data('journals', resource_id=1)
        self.assertIn('title', res)

    def test_fetch_data_with_querystring_params(self):
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber(1)
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey',
                         username='any.username',
                         collection='saude-publica')
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', slumber_dep=mock_slumber)

        res = conn.fetch_data('journals', resource_id=1, collection='saude-publica')
        self.assertIn('title', res)

    def test_unsupported_api_version_raises_ValueError(self):
        mock_slumber = self.mocker.mock()
        self.mocker.replay()

        self.assertRaises(ValueError,
            lambda: self._makeOne('any.username',
                                  'any.apikey',
                                  slumber_dep=mock_slumber,
                                  version='vFoo'))

    def test_unsupported_api_version_at_API_VERSIONS_raises_RequestError(self):
        import scieloapi, slumber
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.throw(slumber.exceptions.HttpClientError)

        self.mocker.replay()

        conn = self._makeOne('any.username', 'any.apikey', slumber_dep=mock_slumber)

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

