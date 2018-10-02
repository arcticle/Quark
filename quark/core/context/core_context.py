import os, six, abc
from datetime import datetime
from future.builtins import super
from quark.core.data.persistence import Persistence, PersistenceType
from quark.core.context import initializers, schemas


@six.add_metaclass(abc.ABCMeta)
class CoreContext(object):
    def __init__(self, directory):

        self.directory = directory
        self.files = {}
        self.storage = None

        self._persistence = Persistence()

    def create_storage(self, filename, schema=None, initializer=None):
        if not self.storage is None:
            raise ValueError("The context has been bound to a storage already.")

        path = os.path.join(self.directory, filename)

        self._validate_path(path)
        
        self.storage = self._persistence.create_storage(path, 
                                                        schema=schema, 
                                                        initializer=initializer)

        return self.storage

    def create_file(self, filename, content=None):
        
        path = os.path.join(self.directory, filename)
        
        self._validate_path(path)

        with self._safe_open(path, "w") as f:
            content = "" if not content else content
            f.write(content)

        file_key = os.path.splitext(filename)[0]

        self.files[file_key] = path

    def _validate_path(self, path):
        if not path.startswith(self.directory):
            raise ValueError("Invalid path.")

    def _safe_open(self, path, mode):
        _dir = os.path.dirname(path)

        if not os.path.exists(_dir):
            os.makedirs(_dir)
        
        return open(path, mode)

    def create_object(self, object_type):
        object_name = str.lower(object_type.__name__)
        store = self._persistence.get_object_store(object_name)
        if store:
            return object_type(store, self)

    @classmethod
    def requires_storage(cls, func):
        def wrapper_func(self, *args, **kwargs):
            if not self.storage:
                raise Exception("Storage hasn't been initialized.")
            return func(self, *args, **kwargs)
        return wrapper_func


class ApplicationContext(CoreContext):
    def __init__(self, directory):
        super().__init__(directory)
        
        self.create_storage(".quarkconfig",
                            schemas.QUARKCONFIG_SCHEMA,
                            initializers.QUARKCONFIG)

    @property
    def workspaces(self):
        return list(self.storage.workspaces)

    @CoreContext.requires_storage
    def get_workspace(self, id=None, name=None, directory=None):
        if id:
            return self._get_workspace_by_id(id)
        
        if name:
            return self._get_workspace_by_id(name)

        if directory:
            return self._get_workspace_by_id(directory)

    @CoreContext.requires_storage
    def create_workspace(self, id, name, directory):
        try:
            self.storage.workspaces.insert({"id":id, "name":name, "dir":directory})
        except:
            return -1

        return id

    @CoreContext.requires_storage
    def delete_workspace(self, id):
        try:
            self.storage.workspaces.delete({"id":id})
        except:
            return -1
        return id


    def _get_workspace_by_id(self, id):
        return self.storage.workspaces.find_one({"id":id})
    
    def _get_workspace_by_name(self, name):
        return self.storage.workspaces.find_one({"name":name})

    def _get_workspace_by_directory(self, directory):
        return self.storage.workspaces.find_one({"dir":directory})


class WorkspaceContext(CoreContext):
    def __init__(self, directory):
        super().__init__(directory)

    @property
    def scripts(self):
        return list(self.storage.scripts)

    @property
    def experiments(self):
        return list(self.storage.experiments)

    @CoreContext.requires_storage
    def create_script(self, script_name, content):
        if script_name in self.storage.scripts:
            raise ValueError("A script with the same name already exists.")

        try:
            self.create_file("scripts\\{}.py".format(script_name), content)
            self.storage.scripts.insert(script_name)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def create_experiment(self, experiment_name):
        if experiment_name in self.storage.experiments:
            raise ValueError("An experiment with the same name already exists.")

        try:
            self.storage.experiments.insert(experiment_name)
        except:
            return -1

        return 1

    @CoreContext.requires_storage
    def delete_experiment(self, experiment_name):
        try:
            self.storage.experiments.delete({"name":experiment_name})
        except:
            return -1
        return 1

    def initialize_storage(self, storage_name):
        filename = "{}.quark".format(storage_name)

        self.create_storage(filename,
                            initializer=initializers.WORKSPACE)


class ExperimentContext(CoreContext):
    def __init__(self, directory):
        super().__init__(directory)

    @property
    def params(self):
        return self.storage.params.to_dict()

    @property
    def pipeline(self):
        return self.storage.pipeline

    @CoreContext.requires_storage
    def add_script(self, script_name):
        try:
            self.storage.pipeline.insert(script_name)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def add_parameter(self, name, value):
        try:
            self.storage.params.set(name, value)
        except:
            return -1
        return 1

    def initialize_storage(self, storage_name):
        filename = "{}.xpr".format(storage_name)

        self.create_storage(filename, 
                            initializer=initializers.EXPERIMENT)


# class RepositoryContext(CoreContext):
#     def __init__(self):
#         super().__init__(default_type=PersistenceType.JSON,
#                          initializer=REPOSITORY)

#     @CoreContext.require_open
#     def create_repository(self):
#         pass

# class ContextType(object):
#     Application = "ApplicationContext"
#     Repository  = "RepositoryContext"



class QuarkContext(object):
    """ A context object used to gain access to repository objects
    to view and manipulate their contents.

    ...

    Attributes
    ----------
    `configuration` : Config
        Quark configuration object

    Methods
    -------
    create_repository(self, name, dir, id=None)
        creates repository object using specified parameters.
 

    """
    def __init__(self, path):
        super().__init__(path,
                         type=PersistenceType.JSON,
                         initializer=QUARKCONFIG)

    @property
    def repositories(self):
        return self.persistence.repositories

    def create_repository(self, name, dir, id=None):
        """ Creates repository object using specified parameters.
        Parameters
        ----------
        `name` : str 
            A friendly name to be given to the repository
        `dir`  : str 
            Directory to maintain the repository files
        `id`   : str, optional 
            Unique ID assigned to the repository  
        
        If the `id` argument is not passed in, an `id` is automatically
        assigned to the repository.

        Returns
        -------
        Repository object if successfully created, else raises RepositoryException
        
        """
        pass

    def remove_repository(self, id):
        """ Removes repository object from the context.
        Parameters
        ----------
        `id`   : str 
            Unique ID of the repository to be deleted

        Returns
        -------
        void
        
        """
        try:
            del self._configuration.repositories[id]
        except:
            from quark.exceptions import RepositoryNotFoundException
            raise RepositoryNotFoundException("Invalid repository ID '{}'. ".format(id) + \
            "Unable to find matching repository for specified ID.")
