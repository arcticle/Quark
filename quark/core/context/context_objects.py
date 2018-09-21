import os
from datetime import datetime
from quark.core.context import ApplicationContext, WorkspaceContext



class Application(object):
    def __init__(self):
        self._context = ApplicationContext()
        self._workspaces = {}

        self.__initialize__()

    @property
    def workspaces(self):
        return self._workspaces

    def create_workspace(self, name, directory):

        workspace_id = datetime.strftime(datetime.now(), r"%Y%m%d%H%M%S")
        result = self._context.create_workspace(int(workspace_id), name, directory)

        if result > 0:
            self._workspaces[result] = Workspace(workspace_id, name, directory)


    def __initialize__(self):
        for ws in self._context.workspaces:
            self._workspaces[ws["id"]] = Workspace(**ws)



class Workspace(object):
    def __init__(self, id, name, dir):
        
        self.id = id
        self.name = name
        self.directory = os.path.join(dir, name)
        
        self._context = WorkspaceContext(name, self.directory)





    

