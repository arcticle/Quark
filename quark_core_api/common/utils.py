from future.utils import viewitems
from future.builtins import super
from collections.abc import Mapping


class Cache(Mapping):
    def __init__(self, *args, **kw):
        self._keys = []
        self._cache = {}
        self._size = 1024

        if args:
            if len(args) > 2:
                raise Exception("Invalid number of arguments have been provided for the cache.")
            self._keys.insert(0, args[0])
            self._cache[args[0]] = args[1]

        if kw:
            for key, value in viewitems(kw):
                if key == "size" and isinstance(value, int):
                    self._size = value
                    continue
                self._keys.insert(len(self._keys), key)
                self._cache[key] = value

    @property
    def items(self):
        return list(self._cache.values())

    def get(self, key):
        return self.__getitem__(key)

    def pop(self, key):
        value = self.__getitem__(key)
        self.__removeitem__(key)
        return value

    def peek(self):
        return self.__getitem__(-1)

    def add(self, key, value):
        self.__additem__(key, value)

    def update(self, key, value):
        _, entry = self.__getentry__(key)
        self._cache[entry] = value

    def remove(self, key):
        self.__removeitem__(key)

    def __getitem__(self, key):
        if key == -1:
            return self._cache[self._keys[-1]]
        
        _, entry = self.__getentry__(key)
        return self._cache[entry]

    def __setitem__(self, key, value):
        if key in self._cache:
            self.update(key, value)
        else:
            self.__additem__(key, value)

    def __additem__(self, key, value):
        n_keys = len(self._keys)

        if n_keys >= self._size:
            raise Exception("Max cache size was reached.")

        self._cache[key] = value
        self._keys.insert(n_keys, key)

    def __removeitem__(self, key):
        index, entry = self.__getentry__(key)
        del self._cache[entry]
        del self._keys[index]

    def __iter__(self):
        for key in self._keys:
            yield key, self._cache[key]
    
    def __len__(self):
        return len(self._keys)

    def __getentry__(self, key):
        if key == -1:
            return (len(self._keys-1), self._keys[-1])

        if isinstance(key, int):
            return (key, self._keys[key])

        if isinstance(key, str):
            return (self._keys.index(key), key)

        raise Exception("Invalid key type provided.")



class ReadOnlyCache(Cache):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def pop(self, key):
        raise Exception("Operation is invalid on ReadOnlyCache.")
    
    def add(self, key, value):
        raise Exception("Operation is invalid on ReadOnlyCache.")

    def update(self, key):
        raise Exception("Operation is invalid on ReadOnlyCache.")

    def remove(self, key):
        raise Exception("Operation is invalid on ReadOnlyCache.")

    def __setitem__(self, key, value):
        raise Exception("Operation is invalid on ReadOnlyCache.")

    def __additem__(self, key, value):
        raise Exception("Operation is invalid on ReadOnlyCache.")

    def __removeitem__(self, key):
        raise Exception("Operation is invalid on ReadOnlyCache.")
