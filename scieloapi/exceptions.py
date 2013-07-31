class ConnectionError(Exception):
    """
    Raised on network problems, e.g. DNS failures, refused connections and so.
    """


class HTTPError(Exception):
    """
    Raised on invalid HTTP responses.
    """


class Timeout(Exception):
    """
    Raised on request timeouts.
    """


class BadRequest(Exception):
    """
    Raised on 400 HTTP status code
    """


class Unauthorized(Exception):
    """
    Raised on 401 HTTP status code
    """


class Forbidden(Exception):
    """
    Raised on 403 HTTP status code
    """


class NotFound(Exception):
    """
    Raised on 404 HTTP status code
    """


class NotAcceptable(Exception):
    """
    Raised on 406 HTTP status code
    """


class InternalServerError(Exception):
    """
    Raised on 500 HTTP status code
    """


class BadGateway(Exception):
    """
    Raised on 502 HTTP status code
    """


class ServiceUnavailable(Exception):
    """
    Raised on 503 HTTP status code
    """

