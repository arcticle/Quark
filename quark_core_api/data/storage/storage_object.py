import six, abc
from future.utils import viewitems
from future.builtins import super
from quark_core_api.data.storage import QueryCommand, ValidationResult
from quark_core_api.common import EventHandler
from quark_core_api.exceptions.storage_exceptions import StorageObjectException


@six.add_metaclass(abc.ABCMeta)
class StorageObject(object):
    def __init__(self, id, storage, validator):
        self.__id__ = id
        self.__storage__ = storage
        self.__validator__ = validator
        self.on_change = EventHandler()

    @property
    def data(self):
        return self.__storage__[self.__id__]

    @data.setter
    def data(self, value):
        self.__storage__[self.__id__] = value

    def _validate(self, data):
        if not self.__validator__:
            return ValidationResult()
            
        return self.__validator__.validate(data, self)


class CollectionObject(StorageObject):
    def __init__(self, id, storage, validator):
        super().__init__(id, storage, validator)

    def find(self, query):
        try:
            items, _ = self._find(query)
            return items
        except Exception as e:
            raise StorageObjectException(
                self.__id__, "find", e)

    def find_one(self, query):
        try:
            cmd = QueryCommand(query)
            for item in self.data:
                result = cmd.execute(item)
                if result == True:
                    return item
        except Exception as e:
            raise StorageObjectException(
                self.__id__, "find_one", e)

    def update(self, query, modifications):
        try:
            _, mask = self._find(query)
            for index, unmasked in enumerate(mask):
                if unmasked:
                    item = self.data[index]
                    if isinstance(item, dict):
                        self._update_dict(item, modifications)
                    else:
                        self.data[index] = modifications
                    self.on_change(self, action="update")
        except Exception as e:
            raise StorageObjectException(
                self.__id__, "update", e)

    def insert(self, obj):
        try:
            validation = self._validate(obj)

            if validation.has_error:
                raise Exception(validation.errors)

            self.data.append(obj)
            self.on_change(self, action="insert")
        except Exception as e:
            raise StorageObjectException(
                self.__id__, "insert", e)


    def delete(self, obj):
        try:
            item = self.find_one(obj)
            self.data.remove(item)
            self.on_change(self, action="delete")
        except Exception as e:
            raise StorageObjectException(
                self.__id__, "delete", e)


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

    def __getitem__(self, index):
        return self.data[index]


class KeyValueObject(StorageObject):
    def __init__(self, id, storage, validator):
        super().__init__(id, storage, validator)
        setattr(self, "value", self.data)

    def __setattr__(self, name, value):
        if name == "value":
            self.data = value
            self.on_change(self, action="update")

        super().__setattr__(name, value)



class ComplexObject(StorageObject):
    def __init__(self, id, storage, validator):
        super().__init__(id, storage, validator)

        for attr, value in viewitems(self.data):
            setattr(self, attr, value)

    def get(self, attr):
        return getattr(self, attr)

    def set(self, attr, value):
        try:
            self.data[attr] = value
            setattr(self, attr, value)
            self.on_change(self, action="update")
            return 1
        except:
            return -1

    def delete(self, attr):
        try:
            del self.data[attr]
            delattr(self, attr)
            self.on_change(self, action="update")
            return 1
        except:
            return -1

    def to_dict(self):
        return dict(self.data)

    def __iter__(self):
        return self.data.__iter__()
