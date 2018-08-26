from copy import deepcopy
from attrdict import AttrDict
from quark.core.data.storage import CollectionObject, ComplexObject, KeyValueObject
from quark.common import EventHandler

class StorageObjectFactory(object):
    def __init__(self, object_types=None):
        self._object_type_map = {}
        if not object_types:
            object_types = self._get_default_object_types()
        self._create_object_type_map(object_types)            
    
    def create(self, id, data):
        value_type = type(data[id])
        storage_object = self._object_type_map[value_type]
        return storage_object(id, data)

    def _create_object_type_map(self, object_types):
        for value_type, object_type in object_types:
            self._object_type_map[value_type] = object_type

    def _get_default_object_types(self):
        yield (list, CollectionObject)
        yield (dict, ComplexObject)
        yield (str, KeyValueObject)
        yield (int, KeyValueObject)
        yield (float, KeyValueObject)
        yield (bool, KeyValueObject)


class Storage(object):
    def __init__(self, data, object_factory=None):
        self._data = data
        self._objects = []
        self.on_change = EventHandler()

        if object_factory is None:
            self._object_factory = StorageObjectFactory()
        else:
            self._object_factory = object_factory
        
        self._create(self._data)

    def _create(self, data):
        for object_name in data:
            storage_object = self._object_factory.create(object_name, data)
            storage_object.on_change += self._on_change
            self._objects.append(object_name)
            setattr(self, object_name, storage_object)

    @property
    def data(self):
        return deepcopy(self._data)

    @property
    def objects(self):
        return self._objects

    def __getitem__(self, key):
        return getattr(self, key)

    def _on_change(self, sender, action=None):
        self.on_change(self)

    
