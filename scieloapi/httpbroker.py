from functools import wraps

import requests

import exceptions


__all__ = ['get']


def check_http_status(response):
    """
    Raises one of `scieloapi.exceptions` depending on response status-code.

    :param response: is a requests.Response instance.
    """
    http_status = response.status_code

    if http_status == 400:
        raise exceptions.BadRequest()
    elif http_status == 401:
        raise exceptions.Unauthorized()
    elif http_status == 403:
        raise exceptions.Forbidden()
    elif http_status == 404:
        raise exceptions.NotFound()
    elif http_status == 406:
        raise exceptions.NotAcceptable()
    elif http_status == 500:
        raise exceptions.InternalServerError()
    elif http_status == 502:
        raise exceptions.BadGateway()
    elif http_status == 503:
        raise exceptions.ServiceUnavailable()
    else:
        return None


def translate_exceptions(func):
    """
    Translates all dependencies' exceptions and re-raise them as scieloapi's.

    This function aims to isolate third-party dependencies from the exposed
    API, in a way users should never import `requests` lib to handle exceptions
    or other stuff.
    """
    @wraps(func)
    def f_wrap(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise exceptions.ConnectionError(e)
        except requests.exceptions.HTTPError as e:
            raise exceptions.HTTPError(e)
        except requests.exceptions.Timeout as e:
            raise exceptions.Timeout(e)
        except requests.exceptions.TooManyRedirects as e:
            raise exceptions.HTTPError(e)
        except requests.exceptions.RequestException as e:
            raise exceptions.HTTPError(e)
        else:
            return resp

    return f_wrap


def _make_full_url(*uri_segs):
    """
    Joins URI segments to produce an URL.

    URI segments are passed as positional args and placed in order
    to produce a valid URL. Trailing slashes and HTTP scheme are
    added automatically.
    """
    full_uri = '/'.join([str(seg).strip('/') for seg in uri_segs if seg])

    if not full_uri.endswith('/'):
        full_uri += '/'
    if not full_uri.startswith('http://'):
        full_uri = 'http://' + full_uri

    return full_uri


@translate_exceptions
def get(api_uri, endpoint=None, resource_id=None, params=None):
    """
    Dispatches an HTTP GET request to `api_uri`.

    This function is tied to some concepts of Restful interfaces
    like endpoints and resource ids. Any querystring params must
    be passed as dictionaries to `params`.

    :param api_uri: e.g. http://manager.scielo.org/api/v1/
    :param endpoint: (optional) a valid endpoint at http://manager.scielo.org/api/v1/
    :param resource_id: (optional) an int representing the document.
    :param params: (optional) params to be passed as query string.
    """
    if not endpoint and resource_id:
        raise ValueError('resource_id depends on an endpoint definition')

    full_uri = _make_full_url(api_uri, endpoint, resource_id)
    resp = requests.get(full_uri, params=params)

    # check if an exception should be raised based on http status code
    check_http_status(resp)

    return resp.json()

