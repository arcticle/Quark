import os, six, abc
from future.builtins import super
from quark.core.data.persistence import Persistence, PersistenceType
from quark.core.context.initializers import QUARKCONFIG



@six.add_metaclass(abc.ABCMeta)
class CoreContext(object):
    def __init__(self, directory):

        self.directory = directory
        self.persistence = Persistence()
        self.files = {}

    def create_storage(self, filename, initializer=None):
        
        path = os.path.join(self.directory, filename)

        self._validate_path(path)
        
        return self.persistence.create_storage(path, initializer=initializer)

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
        store = self.persistence.get_object_store(object_name)
        if store:
            return object_type(store, self)

    @classmethod
    def require_open(cls, func):
        def wrapper_func(self, *args, **kwargs):
            if not self.persistence:
                raise Exception("Context is not open.")
            return func(self, *args, **kwargs)
        return wrapper_func


class ApplicationContext(object):
    def __init__(self):
        directory = os.path.expanduser("~\\")
        self._core_context = CoreContext(directory)
        self._core_context.create_storage(".quarkconfig", QUARKCONFIG)
        self._quark = self._core_context.persistence._quarkconfig 

    @property
    def workspaces(self):
        return list(self._quark.workspaces)

    def create_workspace(self, id, name, directory):
        ws = self._quark.workspaces.find_one({"id":id})
        
        if ws: return None

        self._quark.workspaces.insert({"id":id, "name":name, "dir":directory})
        return id


class WorkspaceContext(object):
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self._core_context = CoreContext(directory)
        self._initialize_storage()


    @property
    def scripts(self):
        return list(self._storage.scripts)

    def create_script(self, script_name, content):
        if script_name in self._storage.scripts:
            raise ValueError("A script with the same name already exists.")
            
        self._core_context.create_file("scripts\\{}.py".format(script_name), content)
        self._storage.scripts.insert(script_name)

    def _initialize_storage(self):
        self._storage = self._core_context.create_storage("{}.quark".format(self.name))
        
        if "scripts" not in self._storage.objects:
            self._storage.add({"scripts":[]})



class RepositoryContext(CoreContext):
    def __init__(self):
        super().__init__(default_type=PersistenceType.JSON,
                         initializer=REPOSITORY)

    @CoreContext.require_open
    def create_repository(self):
        pass

class ContextType(object):
    Application = "ApplicationContext"
    Repository  = "RepositoryContext"






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
