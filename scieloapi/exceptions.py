class APIError(Exception):
    """
    Base class for all API exceptions
    """


class ConnectionError(APIError):
    """
    Raised on network problems, e.g. DNS failures, refused connections and so.
    """


class HTTPError(APIError):
    """
    Raised on invalid HTTP responses.
    """


class Timeout(APIError):
    """
    Raised on request timeouts.
    """


class BadRequest(APIError):
    """
    Raised on 400 HTTP status code
    """


class Unauthorized(APIError):
    """
    Raised on 401 HTTP status code
    """


class Forbidden(APIError):
    """
    Raised on 403 HTTP status code
    """


class NotFound(APIError):
    """
    Raised on 404 HTTP status code
    """


class MethodNotAllowed(APIError):
    """
    Raised on 405 HTTP status code
    """


class NotAcceptable(APIError):
    """
    Raised on 406 HTTP status code
    """


class InternalServerError(APIError):
    """
    Raised on 500 HTTP status code
    """


class BadGateway(APIError):
    """
    Raised on 502 HTTP status code
    """


class ServiceUnavailable(APIError):
    """
    Raised on 503 HTTP status code
    """

