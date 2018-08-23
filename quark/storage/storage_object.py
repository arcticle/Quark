import six, abc
from future.utils import viewitems
from future.builtins import super
from quark.storage.query import QueryCommand



@six.add_metaclass(abc.ABCMeta)
class StorageObject(object):
    def __init__(self, id, storage):
        self.__id__ = id
        self.__storage__ = storage

    @property
    def data(self):
        return self.__storage__[self.__id__]

    @data.setter
    def data(self, value):
        self.__storage__[self.__id__] = value 


class CollectionObject(StorageObject):
    def __init__(self, id, storage):
        super().__init__(id, storage)

    def find(self, query):
        items, _ = self._find(query)
        return items

    def find_one(self, query):
        cmd = QueryCommand(query)
        for item in self.data:
            if cmd.execute(item):
                return item

    def update(self, query, modifications):
        _, mask = self._find(query)
        for index, unmasked in enumerate(mask):
            if unmasked:
                item = self.data[index]
                if isinstance(item, dict):
                    self._update_dict(item, modifications)
                else:
                    self.data[index] = modifications

    def create(self, obj):
        self.data.append(obj)

    def delete(self, obj):
        item = self.find(obj)
        self.data.remove(item)

    def _find(self, query):
        items, mask = [], []
        cmd = QueryCommand(query)
        for item in self.data:
            result = cmd.execute(item)
            if result == True:    
                items.append(item)
            mask.append(result)
        return items, mask

    def _update_dict(self, dict, modifications):
        for key, value in viewitems(modifications):
            if key in dict:
                dict[key] = value

    def __iter__(self):
        return self.data.__iter__()


class KeyValueObject(StorageObject):
    def __init__(self, id, storage):
        super().__init__(id, storage)
        setattr(self, "value", self.data)

    def __setattr__(self, name, value):
        if name == "value":
            self.data = value
        super().__setattr__(name, value)



class ComplexObject(StorageObject):
    def __init__(self, id, storage):
        super().__init__(id, storage)

        for attr, value in viewitems(self.data):
            setattr(self, attr, value)

    def get(self, attr):
        return getattr(self, attr)

    def set(self, attr, value):
        self.data[attr] = value
        setattr(self, attr, value)