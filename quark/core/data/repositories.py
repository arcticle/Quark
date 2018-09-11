import os
from quark.core.data.persistence import Persistence, PersistenceType
from quark.core.context import initializers




class QuarkRepository(object):
    ''' Persistent repository object for Quark configuration data  '''

    def __init__(self, path):
        self._persistence = \
            Persistence(path,
                        default_type=PersistenceType.JSON,
                        initializer=initializers.QUARKCONFIG,
                        auto_create=True)

    @property
    def workspaces(self):
        return self._persistence._quarkconfig.workspaces




class RepositoryManager(object):
    _repositories = {
        QuarkRepository : os.path.expanduser(r"~\.quarkconfig")
    }

    @staticmethod
    def get(self, repository):
        if repository in RepositoryManager._repositories:
            path = RepositoryManager._repositories[repository]
            return repository(path)
        
        raise ValueError("Invalid repository type has been specified")