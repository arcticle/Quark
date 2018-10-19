import os, six, abc
from copy import deepcopy
from attrdict import AttrDict
from future.utils import viewitems
from future.builtins import super
from app_settings import Config
from quark_core_api.data.storage import CollectionObject, ComplexObject, KeyValueObject, Validator
from quark_core_api.common import DelayedEventHandler
from quark_core_api.exceptions import InvalidOperationException

class StorageObjectFactory(object):
    def __init__(self, object_types=None):
        self._object_type_map = {}
        if not object_types:
            object_types = self._get_default_object_types()
        self._create_object_type_map(object_types)            
    
    def create(self, id, data, validator):
        value_type = type(data[id])
        storage_object = self._object_type_map[value_type]
        return storage_object(id, data, validator)

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

@six.add_metaclass(abc.ABCMeta)
class StorageBase(object):
    def __init__(self, data, schema=None):
        self.__data__ = data
        self.__schema__ = schema
        self.__objects__ = []
        self._object_factory = StorageObjectFactory()

        self.object_changed = DelayedEventHandler()

        self._create_objects(data, schema)


    @property
    def data(self):
        return deepcopy(self.__data__)

    @property
    def schema(self):
        return deepcopy(self.__schema__)

    @property
    def entries(self):
        return deepcopy(self.__objects__)

    def create_entry(self, data, schema=None):
        for object_name, value in viewitems(data):
            if object_name in self.__data__:
                raise InvalidOperationException(
                    "Invalid data provided. Key already exists.")
            self.__data__[object_name] = value
        self._create_objects(data, schema)

    def _create_objects(self, data, schema):
        for object_name in data:
            if schema and object_name in schema:
                validator = Validator(schema[object_name])
            else:
                validator = None
            storage_object = self._object_factory.create(object_name, data, validator)
            storage_object.on_change += self._on_object_change
            self.__objects__.append(object_name)
            setattr(self, object_name, storage_object)
            self.object_changed(storage_object)

    def _on_object_change(self, sender, action=None):
        self.object_changed(self, changed_object=sender)

    def __getitem__(self, key):
        return getattr(self, key)


class InMemoryStorage(StorageBase):
    def __init__(self, name, data, schema=None):
        super().__init__(AttrDict(data), schema=schema)

        self.name = name


class FileStorage(StorageBase):
    def __init__(self,
                 path, 
                 default_type=None, 
                 initializer=None,
                 schema=None,
                 auto_create=False):
        
        self._path = path

        file_exists = os.path.isfile(path)
        
        self._filestore = Config(path, 
                                 default=default_type, 
                                 auto_create=auto_create)
        
        self.name = self._filestore.files[0]

        if not file_exists and initializer:
            self._initialize(initializer)
            self._filestore.save_all()

        super().__init__(self._filestore[self.name], schema)

    def _on_object_change(self, sender, action=None):
        self._filestore.save_all()
        super()._on_object_change(sender, action=action)

    def _initialize(self, initializer):
        for object_name, value in viewitems(initializer):
            if not object_name in self._filestore[self.name]:
                self._filestore[self.name][object_name] = value


    
