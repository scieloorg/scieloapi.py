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

