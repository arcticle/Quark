import os, six, abc
from quark.context.configuration import QuarkConfiguration



def Context():
    return ContextFactory().create()



class ContextFactory(object):

    configuration_file_path = os.path.expanduser("~/.quarkconfig")
    configuration_file_type = "json"

    def create(self):
        return QuarkContext(
            QuarkConfiguration(
                self.configuration_file_path, 
                self.configuration_file_type))





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
    def __init__(self, configuration):
        self._configuration = configuration

    @property
    def repositories(self):
        return self._configuration.repositories.copy()

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
