import os, six, abc
from app_settings import Config
from future.utils import viewitems
from future.builtins import super
from quark.repository import RepositoryFactory
from quark.context.storage import Storage, RepositoryCollection


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
        A dict like object to including initial 
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

        self._storages = {}

        self._config = Config(path, 
                              default=default_type, 
                              auto_create=auto_create)

        if initializer:
            self._initialize(initializer)

        for file in self._config.files:
            storage = self._create_storage(file)
            storage.storage_changed += self._on_storage_update
            self._storages[file] = storage

    def _initialize(self, initializer):
        for section, items in viewitems(initializer):
            for section_item, initial_value in viewitems(items):
                if not section_item in self._config[section]:
                    self._config[section][section_item] = initial_value

    def _create_storage(self, config_section):
        return Storage(config_section, self._config[config_section])

    def _on_storage_update(self, sender):
        self._config.save(sender.name)


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

configuration_file_path = os.path.expanduser("~/.quarkconfig")
c = QuarkConfiguration(configuration_file_path, "json")

class aa(object):
    def __init__(self):
        self.name = "deneme4"
        self.dir = "aşsldjaşlsdjalsd"
        self.id = "a0ea06459d3648cea05ca158d725416d"
    
    @property
    def resource_uri(self):
        return "repositories"

print(c.get(aa()))