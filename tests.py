# coding: utf-8
import mocker


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
