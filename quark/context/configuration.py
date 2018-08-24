import os, six, abc
from app_settings import Config
from future.utils import viewitems
from future.builtins import super
from quark.repository import RepositoryFactory
from quark.storage import Storage


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

        self._stores = {}

        self._filestore = Config(path, 
                                 default=default_type, 
                                 auto_create=auto_create)

        if initializer:
            self._initialize(initializer)

        for f in self._filestore.files:
            storage = Storage(self._filestore[f])
            storage.on_change += self._on_storage_change
            self._stores[storage] = f
            setattr(self, f, storage)


    def _initialize(self, initializer):
        for store, data in viewitems(initializer):
            for object_data, initial_value in viewitems(data):
                if not object_data in self._filestore[store]:
                    self._filestore[store][object_data] = initial_value

    def _on_storage_change(self, sender):
        self._filestore.save(self._stores[sender])


class QuarkConfiguration(object):
    """ An high level configuration object containing
    and exposing application specific data.

    Parameters
    ----------
    `path` : str
        Full path to the configuration file 
        including the file name

    `file_type` : str
        Type of underlying configuration file.
        
    `json` and `yaml` files supported currently

    Attributes
    ----------
    `repositories` : RepositoryCollection
        Collection of repositories initialized
    """
    storage_initializer = dict(_quarkconfig=dict(repositories=[]))
    
    def __init__(self, path, file_type):
        self._persistence = \
            Persistence(path,
                        initializer=self.storage_initializer,
                        default_type=self._file_type_handler(file_type),
                        auto_create=True)

        self._storage = self._persistence._storages["_quarkconfig"]
        self._storage.create_collection("repositories", RepositoryCollection)

    @property
    def repositories(self):
        return self._storage.repositories

    def _file_type_handler(self, file_type):
        def handler(filename):
            return file_type
        return handler

    def get(self, obj):
        return self._storage.get(obj)
