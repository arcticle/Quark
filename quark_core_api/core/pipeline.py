import os, copy
from future.utils import viewitems
from quark_core_api.common import Cache


class Pipeline(object):
    def __init__(self, *args, **kw):
        self._params = {}
        self._cache = Cache()

        if args:
            for script in args:
                self._cache.add(script.name, script)
        if kw:
            for name, value in viewitems(kw):
                if name == "params":
                    self._params = value
                else:
                    self._cache.add(name, value)

    @property
    def params(self):
        return copy.deepcopy(self._params)

    @property
    def steps(self):
        return [value for key, value in self._cache]

    def add_step(self, script):
        self._cache.add(script.name, script)

    def add_param(self, name, value):
        self._params[name] = value

    def __getitem__(self, key):
        return self._cache.get(key)

    def __iter__(self):
        return self._cache.__iter__()
    
    def __len__(self):
        return len(self._cache)


