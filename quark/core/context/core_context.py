import os, six, abc
from future.builtins import super
from quark.core.data.persistence import Persistence, PersistenceType
from quark.core.context.initializers import QUARKCONFIG, REPOSITORY



@six.add_metaclass(abc.ABCMeta)
class CoreContext(object):
    def __init__(self, 
                 persistence_type, 
                 initializer=None):
        
        self._type = persistence_type
        self._initializer = initializer

    def open(self, path):
        self.persistence = Persistence(path,
                                       initializer=self._initializer,
                                       default_type=self._type,
                                       auto_create=True)

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


class ApplicationContext(CoreContext):
    def __init__(self):
        super().__init__(default_type=PersistenceType.JSON,
                         initializer=QUARKCONFIG)


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
