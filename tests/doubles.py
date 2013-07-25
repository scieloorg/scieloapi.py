# coding: utf-8
import types


class Patch(object):
    """
    Helps patching instances to ease testing.
    """
    def __init__(self, target_object, target_attrname, patch):
        self.target_object = target_object
        self.target_attrname = target_attrname
        if callable(patch):
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

