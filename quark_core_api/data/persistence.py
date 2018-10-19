import os, six, abc, copy
from app_settings import Config
from future.utils import viewitems
from future.builtins import super
from quark_core_api.data.storage import FileStorage, InMemoryStorage


class PersistenceType(object):
    JSON = "json"
    YAML = "yaml"

class Persistence(object):
    """ `Internal use only`

    A configuration object providing basic functionality for 
    configuration management. The underlying `Config` object from app_settings
    library keeps application settings up-to-date including the runtime manipulations
    performed on configuration data.

    Parameters
    ----------
    `path` : str
        Full path to the configuration file 
        including the file name

    `initializer` : dict
        A dict like object including initial 
        configuration values

    `default_type` : callable
        Specifies default file type if the type can't be resolved
    
    `auto_create` : bool
        Specifies whether the configuration file 
        to be created if not exist
    """
    def __init__(self):

        self._stores = {}

    def create_storage(self, filename, initializer=None, schema=None, default_type=None, in_mem=False):
        _file_type = "json" if not default_type else default_type 
        _type_handler = lambda t : _file_type

        return self._create_storage(filename, _type_handler, initializer, schema, in_mem)

    def get_object_store(self, object_name):
        for name, store in viewitems(self._stores):
            if object_name in store.objects:
                return name

    @property
    def stores(self):
        return self._stores


    def _create_storage(self, filename, type_handler, initializer, schema, in_mem):
        try:
            if in_mem:
                data = {} if initializer is None else copy.deepcopy(initializer)
                storage = self._create_in_memory_storage(filename, data, schema)
            else:
                storage = self._create_file_storage(filename, type_handler, initializer, schema)
            
            self._on_storage_create(storage)
        except:
            return None
        return storage


    def _create_in_memory_storage(self, storage_name, data, schema):
        return InMemoryStorage(storage_name, data, schema=schema)

    def _create_file_storage(self, path, type_handler, initializer=None, schema=None):
        return FileStorage(path, 
                           default_type=type_handler,
                           initializer=initializer,
                           schema=schema,
                           auto_create=True)

    def _on_storage_create(self, storage):
        self._stores[storage.name] = storage
        setattr(self, storage.name, storage)

