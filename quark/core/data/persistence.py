import os, six, abc
from app_settings import Config
from future.utils import viewitems
from future.builtins import super
from quark.core.data.storage import Storage


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
    def __init__(self, 
                 path, 
                 initializer=None, 
                 default_type=None, 
                 auto_create=None):

        default = lambda t: default_type

        self._stores = {}

        self._filestore = Config(path,
                                 default=default, 
                                 auto_create=auto_create)

        if initializer:
            self._initialize(initializer)

        for f in self._filestore.files:
            storage = Storage(self._filestore[f])
            storage.on_change += self._on_storage_change
            self._stores[storage] = f
            setattr(self, f, storage)

    def get_object_store(self, object_name):
        for name, store in viewitems(self._stores):
            if object_name in store.objects:
                return name

    def _initialize(self, initializer):
        for store, data in viewitems(initializer):
            for object_data, initial_value in viewitems(data):
                if not object_data in self._filestore[store]:
                    self._filestore[store][object_data] = initial_value

    def _on_storage_change(self, sender):
        self._filestore.save(self._stores[sender])
