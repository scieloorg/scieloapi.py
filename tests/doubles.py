# coding: utf-8
import types


class Patch(object):
    """
    Helps patching instances to ease testing.
    """
    def __init__(self, target_object, target_attrname, patch, instance_method=False):
        self.target_object = target_object
        self.target_attrname = target_attrname
        if callable(patch) and instance_method:
            self.patch = types.MethodType(patch, target_object, target_object.__class__)
        else:
            self.patch = patch
        self._toggle()

    def _toggle(self):
        self._x = getattr(self.target_object, self.target_attrname)

        setattr(self.target_object, self.target_attrname, self.patch)
        self.patch = self._x

    def __enter__(self):
        return self.target_object

    def __exit__(self, *args, **kwargs):
        self._toggle()


class ConnectorStub(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_endpoints(self):
        return {'journals': None}

    def fetch_data(self, *args, **kwargs):
        pass


class TimeStub(object):

    @staticmethod
    def sleep(*args):
        pass


class RequestsResponseStub(object):
    """
    Pretend to be a requests.Response object.
    """
    def __init__(self, *args, **kwargs):
        self.status_code = 200


httpbroker_stub = types.ModuleType('httpbroker')
httpbroker_stub.get = lambda *args, **kwargs: {}
httpbroker_stub.post = lambda *args, **kwargs: 'http://manager.scielo.org/api/v1/journals/32/'

