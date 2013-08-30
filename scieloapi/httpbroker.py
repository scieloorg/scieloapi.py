import json
from functools import wraps

import requests

from . import exceptions
from . import __user_agent__


__all__ = ['get', 'post']


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
    elif http_status == 405:
        raise exceptions.MethodNotAllowed()
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


def prepare_params(params):
    """
    Prepare params before the http request is dispatched.

    The return value must be a list of doubles (tuples of lenght 2). By now,
    the preparation step basically transforms `params` to the right return type
    sorted by keys.

    In cases where `params` is None, None must be returned.

    :param params: Is key/value pair or `None`.
    """
    if params is None:
        return None

    if hasattr(params, 'items'):
        params = params.items()

    return sorted(params)


def prepare_data(data):
    """
    Prepare data to be dispatched.

    If `data` is a byte string, nothing is done, else `data` is
    encoded as JSON.

    :param data: json serializable data
    """
    prepared = data if isinstance(data, basestring) else json.dumps(data)
    return prepared



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


class ApiKeyAuth(requests.auth.AuthBase):
    """
    ApiKey based authentication for `requests`.
    """
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def __call__(self, r):
        """
        Adds the Authorization header as listed in
        http://ref.scielo.org/ddkpmx
        """
        auth_string = ' ApiKey %s:%s' % (self.username, self.api_key)
        r.headers['Authorization'] = auth_string
        return r


@translate_exceptions
def get(api_uri, endpoint=None, resource_id=None, params=None, auth=None):
    """
    Dispatches an HTTP GET request to `api_uri`.

    This function is tied to some concepts of Restful interfaces
    like endpoints and resource ids. Any querystring params must
    be passed as dictionaries to `params`.

    :param api_uri: e.g. http://manager.scielo.org/api/v1/
    :param endpoint: (optional) a valid endpoint at http://manager.scielo.org/api/v1/
    :param resource_id: (optional) an int representing the document.
    :param params: (optional) params to be passed as query string.
    :param auth: (optional) a pair of `username` and `api_key`.
    """
    if not endpoint and resource_id:
        raise ValueError('resource_id depends on an endpoint definition')

    if auth:
        username, api_key = auth
    else:
        username = api_key = None

    full_uri = _make_full_url(api_uri, endpoint, resource_id)

    # custom headers
    headers = {'User-Agent': __user_agent__}

    optionals = {}
    if username and api_key:
        optionals['auth'] = ApiKeyAuth(username, api_key)

    resp = requests.get(full_uri,
                        headers=headers,
                        params=prepare_params(params),
                        **optionals)

    # check if an exception should be raised based on http status code
    check_http_status(resp)

    return resp.json()


def post(api_uri, data, endpoint=None, auth=None):
    """
    Dispatches an HTTP POST request to `api_uri`, with `data`.

    This function is tied to some concepts of Restful interfaces
    like endpoints. A new resource is created and its URL is
    returned.

    :param api_uri: e.g. http://manager.scielo.org/api/v1/
    :param data: json serializable Python datastructures.
    :param endpoint: (optional) a valid endpoint at http://manager.scielo.org/api/v1/
    :param auth: (optional) a pair of `username` and `api_key`.
    :returns: newly created resource url
    """
    if auth:
        username, api_key = auth
    else:
        username = api_key = None

    full_url = _make_full_url(api_uri, endpoint)

    # custom headers
    headers = {'User-Agent': __user_agent__}

    optionals = {}
    if username and api_key:
        optionals['auth'] = ApiKeyAuth(username, api_key)

    resp = requests.post(url=full_url,
                         data=prepare_data(data),
                         headers=headers,
                         **optionals)

    # check if an exception should be raised based on http status code
    check_http_status(resp)

    if resp.status_code != 201:
        raise exceptions.APIError('The server gone nuts: %s' % resp.status_code)

    return resp.headers['location']

