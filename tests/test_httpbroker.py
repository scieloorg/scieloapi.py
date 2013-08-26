import unittest

import mocker

from scieloapi import httpbroker, exceptions
import doubles


class CheckHttpStatusTests(unittest.TestCase):

    def test_400_raises_BadRequest(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 400

        self.assertRaises(exceptions.BadRequest,
            lambda: httpbroker.check_http_status(response))

    def test_401_raises_Unauthorized(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 401

        self.assertRaises(exceptions.Unauthorized,
            lambda: httpbroker.check_http_status(response))

    def test_403_raises_Forbidden(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 403

        self.assertRaises(exceptions.Forbidden,
            lambda: httpbroker.check_http_status(response))

    def test_404_raises_NotFound(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 404

        self.assertRaises(exceptions.NotFound,
            lambda: httpbroker.check_http_status(response))

    def test_406_raises_NotAcceptable(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 406

        self.assertRaises(exceptions.NotAcceptable,
            lambda: httpbroker.check_http_status(response))

    def test_500_raises_InternalServerError(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 500

        self.assertRaises(exceptions.InternalServerError,
            lambda: httpbroker.check_http_status(response))

    def test_502_raises_BadGateway(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 502

        self.assertRaises(exceptions.BadGateway,
            lambda: httpbroker.check_http_status(response))

    def test_503_raises_ServiceUnavailable(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 503

        self.assertRaises(exceptions.ServiceUnavailable,
            lambda: httpbroker.check_http_status(response))

    def test_200_returns_None(self):
        response = doubles.RequestsResponseStub()
        response.status_code = 200

        self.assertIsNone(httpbroker.check_http_status(response))


class TranslateExceptionsTests(unittest.TestCase):

    def test_from_ConnectionError_to_ConnectionError(self):
        """
        from requests.exceptions.ConnectionError
        to scieloapi.exceptions.ConnectionError
        """
        import requests

        @httpbroker.translate_exceptions
        def foo():
            raise requests.exceptions.ConnectionError()

        self.assertRaises(exceptions.ConnectionError,
            lambda: foo())

    def test_from_HTTPError_to_HTTPError(self):
        """
        from requests.exceptions.HTTPError
        to scieloapi.exceptions.HTTPError
        """
        import requests

        @httpbroker.translate_exceptions
        def foo():
            raise requests.exceptions.HTTPError()

        self.assertRaises(exceptions.HTTPError,
            lambda: foo())

    def test_from_Timeout_to_Timeout(self):
        """
        from requests.exceptions.Timeout
        to scieloapi.exceptions.Timeout
        """
        import requests

        @httpbroker.translate_exceptions
        def foo():
            raise requests.exceptions.Timeout()

        self.assertRaises(exceptions.Timeout,
            lambda: foo())

    def test_from_TooManyRedirects_to_HTTPError(self):
        """
        from requests.exceptions.TooManyRedirects
        to scieloapi.exceptions.HTTPError
        """
        import requests

        @httpbroker.translate_exceptions
        def foo():
            raise requests.exceptions.TooManyRedirects()

        self.assertRaises(exceptions.HTTPError,
            lambda: foo())

    def test_from_RequestException_to_HTTPError(self):
        """
        from requests.exceptions.RequestException
        to scieloapi.exceptions.HTTPError
        """
        import requests

        @httpbroker.translate_exceptions
        def foo():
            raise requests.exceptions.RequestException()

        self.assertRaises(exceptions.HTTPError,
            lambda: foo())


class PrepareParamsFunctionTests(unittest.TestCase):

    def test_sort_dict_by_key(self):
        params = {'username': 1, 'api_key': 2, 'c': 3}

        self.assertEqual(httpbroker.prepare_params(params),
            [('api_key', 2), ('c', 3), ('username', 1)])

    def test_sort_list_of_tuples(self):
        params = [('username', 1), ('api_key', 2), ('c', 3)]

        self.assertEqual(httpbroker.prepare_params(params),
            [('api_key', 2), ('c', 3), ('username', 1)])

    def test_None_returns_None(self):
        params = None

        self.assertIsNone(httpbroker.prepare_params(params))


