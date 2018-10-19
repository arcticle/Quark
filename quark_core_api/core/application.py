import os
from datetime import datetime
from quark_core_api.context import ApplicationContext, WorkspaceContext
from quark_core_api.common import ContextInitializer
from quark_core_api.core import QuarkWorkspace
from quark_core_api.exceptions import InvalidContextException


class QuarkApplication(object):
    def __init__(self, context):
        if not isinstance(context, ApplicationContext):
            raise InvalidContextException(context)

        self._context = context
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
            ctx = WorkspaceContext(ws_dir, ContextInitializer.workspace)
            ws = QuarkWorkspace(ws_id, name, ctx)

            self._workspaces[result] = ws
            return ws

    def delete_workspace(self, id):
        result = self._context.delete_workspace(int(id))

        if result > 0:
            del self._workspaces[id]


    def __initialize__(self):
        self._context.create_storage(".quarkconfig")

        for ws in self._context.workspaces:
            ctx = WorkspaceContext(ws["dir"], ContextInitializer.workspace)
            args = (ws["id"], ws["name"], ctx)
            self._workspaces[ws["id"]] = QuarkWorkspace(*args)
