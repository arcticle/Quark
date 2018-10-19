import os, six, abc
from quark_core_api.data.persistence import Persistence
from quark_core_api.exceptions import InvalidOperationException


@six.add_metaclass(abc.ABCMeta)
class CoreContext(object):
    def __init__(self, directory, context_initializer):

        self.directory = directory
        self.initializer = context_initializer

        self.files = {}
        self.storage = None
        self.storage_type = None

        self._persistence = Persistence()

    def create_storage(self, filename):
        if not self.storage is None:
            raise InvalidOperationException(
                "The context has already been bound to a storage.")

        try:
            self.storage_type = "file"
            path = os.path.join(self.directory, filename)
            self._validate_path(path)
            self.storage = self._persistence.create_storage(path, 
                                                            schema=self.initializer.schema, 
                                                            initializer=self.initializer.object_initializer)
        except:
            self.storage_type = "memory"
            self.storage = self._persistence.create_storage(filename, 
                                                            schema=self.initializer.schema,
                                                            initializer=self.initializer.object_initializer,
                                                            in_mem=True)
        
        self.storage.object_changed += self._on_storage_change
        
        return self.storage

    def create_file(self, filename, content=None):
        path = filename

        if self.storage_type == "file":
            path = os.path.join(self.directory, filename)
            self._validate_path(path)

        with self._safe_open(path, "w") as f:
            content = "" if not content else content
            f.write(content)

        file_key = os.path.splitext(filename)[0]

        self.files[file_key] = path

    def _validate_path(self, path):
        if not path.startswith(self.directory):
            raise InvalidOperationException("Invalid path.")

    def _safe_open(self, path, mode):
        _dir = os.path.dirname(path)

        if not os.path.exists(_dir):
            os.makedirs(_dir)
        
        return open(path, mode)

    def _on_storage_change(self, changed_object):
        pass

    def create_object(self, object_name, value, schema=None):
        self.storage.create_entry({object_name:value}, schema=schema)

    @classmethod
    def requires_storage(cls, func):
        def wrapper_func(self, *args, **kwargs):
            if not self.storage:
                raise InvalidOperationException(
                    "Storage hasn't been initialized.")
            return func(self, *args, **kwargs)
        return wrapper_func


# class QuarkContext(object):
#     """ A context object used to gain access to repository objects
#     to view and manipulate their contents.

#     ...

#     Attributes
#     ----------
#     `configuration` : Config
#         Quark configuration object

#     Methods
#     -------
#     create_repository(self, name, dir, id=None)
#         creates repository object using specified parameters.
 

#     """
#     def __init__(self, path):
#         super().__init__(path,
#                          type=PersistenceType.JSON,
#                          initializer=QUARKCONFIG)

#     @property
#     def repositories(self):
#         return self.persistence.repositories

#     def create_repository(self, name, dir, id=None):
#         """ Creates repository object using specified parameters.
#         Parameters
#         ----------
#         `name` : str 
#             A friendly name to be given to the repository
#         `dir`  : str 
#             Directory to maintain the repository files
#         `id`   : str, optional 
#             Unique ID assigned to the repository  
        
#         If the `id` argument is not passed in, an `id` is automatically
#         assigned to the repository.

#         Returns
#         -------
#         Repository object if successfully created, else raises RepositoryException
        
#         """
#         pass

#     def remove_repository(self, id):
#         """ Removes repository object from the context.
#         Parameters
#         ----------
#         `id`   : str 
#             Unique ID of the repository to be deleted

#         Returns
#         -------
#         void
        
#         """
#         try:
#             del self._configuration.repositories[id]
#         except:
#             from quark.exceptions import RepositoryNotFoundException
#             raise RepositoryNotFoundException("Invalid repository ID '{}'. ".format(id) + \
#             "Unable to find matching repository for specified ID.")
