import os
from datetime import datetime
from quark_core_api.context import ApplicationContext, WorkspaceContext
from quark_core_api.core import QuarkWorkspace


class QuarkApplication(object):
    def __init__(self):
        app_dir = os.path.expanduser("~\\")
        self._context = ApplicationContext(app_dir)
        self._workspaces = {}

        self.__initialize__()

    @property
    def workspaces(self):
        return self._workspaces

    def create_workspace(self, name, directory):

        ws_id = datetime.strftime(datetime.now(), r"%Y%m%d%H%M%S")
        ws_dir = os.path.join(directory, name)
        result = self._context.create_workspace(int(ws_id), name, ws_dir)

        if result > 0:
            ws = QuarkWorkspace(ws_id, name, WorkspaceContext(ws_dir))
            self._workspaces[result] = ws
            return ws

    def delete_workspace(self, id):
        result = self._context.delete_workspace(int(id))

        if result > 0:
            del self._workspaces[id]


    def __initialize__(self):
        for ws in self._context.workspaces:
            args = (ws["id"], ws["name"], WorkspaceContext(ws["dir"]))
            self._workspaces[ws["id"]] = QuarkWorkspace(*args)
