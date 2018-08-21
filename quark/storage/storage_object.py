import six, abc
from future.utils import viewitems
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
        items = []
        cmd = QueryCommand(query)
        for item in self.data:
            if cmd.execute(item):
                items.append(item)
        return items

    def find_one(self, query):
        cmd = QueryCommand(query)
        for item in self.data:
            if cmd.execute(item):
                return item

    def update(self, query, modifications):
        items = self.find(query)
        for item in items:
            self._update_dict(item, modifications)

    def create(self, obj):
        self.data.append(obj)

    def delete(self, obj):
        item = self.find(obj)
        self.data.remove(item)

    def _update_dict(self, dict, modifications):
        for key, value in viewitems(modifications):
            if key in dict:
                dict[key] = value

    def _get_dict_item(self, item, obj):
        obj_elements = set(viewitems(obj))
        item_elements = set(viewitems(item))
        intersection = item_elements.union(obj_elements)
        if len(intersection) <= len(item):
            return item

    def __iter__(self):
        return self.data.__iter__()


class KeyValueObject(StorageObject):
    def __init__(self, id, storage):
        super().__init__(id, storage)

    def get(self):
        return self.data

    def update(self, value):
        self.data = value


class ComplexObject(StorageObject):
    def __init__(self, id, storage):
        super().__init__(id, storage)

        for attr, value in viewitems(self.data):
            setattr(self, attr, value)

    def get(self, obj):
        return getattr(self, obj)

    def update(self, obj, value):
        self.data[obj] = value
        setattr(self, obj, value)