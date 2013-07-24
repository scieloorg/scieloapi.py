import requests


def _make_full_uri(*path_segs):
    full_uri = '/'.join([str(seg).strip('/') for seg in path_segs if seg])

    if not full_uri.endswith('/'):
        full_uri += '/'
    if not full_uri.startswith('http://'):
        full_uri = 'http://' + full_uri

    return full_uri


def get(api_uri, endpoint=None, resource_id=None, params=None):
    if not endpoint and resource_id:
        raise ValueError('resource_id depends on an endpoint definition')

    full_uri = _make_full_uri(api_uri, endpoint, resource_id)
    resp = requests.get(full_uri, params=params)

    return resp.json()

