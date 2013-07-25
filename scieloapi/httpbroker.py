import requests


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


def get(api_uri, endpoint=None, resource_id=None, params=None):
    """
    Dispatches an HTTP GET request to `api_uri`.

    This function is tied to some concepts of Restful interfaces
    like endpoints and resource ids. Any querystring params must
    be passed as dictionaries to `params`.
    """
    if not endpoint and resource_id:
        raise ValueError('resource_id depends on an endpoint definition')

    full_uri = _make_full_url(api_uri, endpoint, resource_id)
    resp = requests.get(full_uri, params=params)

    return resp.json()

