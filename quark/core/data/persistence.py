import os, six, abc
from app_settings import Config
from future.utils import viewitems
from future.builtins import super
from quark.core.data.storage import Storage, FileStorage


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

        self._default = lambda t: default_type
        self._auto_create = auto_create

        self._stores = {}

        # self._filestore = Config(path,
        #                          default=self._default, 
        #                          auto_create=auto_create)

        # if initializer:
        #     self._initialize(initializer)

        # for f in self._filestore.files:
        #     storage = Storage(self._filestore[f])
        #     storage.on_change += self._on_storage_change
        #     self._stores[storage] = f
        #     setattr(self, f, storage)

        storage = FileStorage(path, default_type=self._default, initializer=initializer)
        setattr(self, storage.name, storage)
        

    def create_storage(self, path=None, directory=None, initializer=None):
        if path:
            self._create_file_storage(path, initializer)
        # elif directory:
        #     self._create_dir_storage(path, initializer)

    def get_object_store(self, object_name):
        for name, store in viewitems(self._stores):
            if object_name in store.objects:
                return name

    def _create_file_storage(self, path, initializer=None):
        if os.path.isfile(path):
            filestore = Config(files=path, default=self._default)
        else:
            filestore = Config(files=path, default=self._default, auto_create=self._auto_create)
            if initializer:
                self._initialize(initializer)

        for f in filestore.files:
            storage = Storage(filestore[f])
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
