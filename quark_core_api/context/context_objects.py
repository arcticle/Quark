from future.builtins import super
from quark_core_api.context import CoreContext
from quark_core_api.exceptions import InvalidOperationException

class ApplicationContext(CoreContext):
    def __init__(self, directory, context_initializer):
        super().__init__(directory, context_initializer)

    @property
    @CoreContext.requires_storage
    def workspaces(self):
        return list(self.storage.workspaces)

    @CoreContext.requires_storage
    def get_workspace(self, id=None, name=None, directory=None):
        if id:
            return self._get_workspace_by_id(id)
        
        if name:
            return self._get_workspace_by_name(name)

        if directory:
            return self._get_workspace_by_directory(directory)

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

    def _on_storage_change(self, changed_object):
        pass


class WorkspaceContext(CoreContext):
    def __init__(self, directory, context_initializer):
        super().__init__(directory, context_initializer)

    @property
    @CoreContext.requires_storage
    def scripts(self):
        return list(self.storage.scripts)

    @property
    @CoreContext.requires_storage
    def experiments(self):
        return list(self.storage.experiments)

    @CoreContext.requires_storage
    def create_script(self, script_name, content):
        if script_name in self.storage.scripts:
            raise InvalidOperationException(
                "A script with the same name already exists.")

        try:
            self.create_file("scripts\\{}.py".format(script_name), content)
            self.storage.scripts.insert(script_name)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def delete_script(self, script_name):
        try:
            self.storage.scripts.delete({"$eq":script_name})
        except:
            return -1
        return 1


    @CoreContext.requires_storage
    def create_experiment(self, experiment_name):
        if experiment_name in self.storage.experiments:
            raise InvalidOperationException(
                "An experiment with the same name already exists.")

        try:
            self.storage.experiments.insert(experiment_name)
        except:
            return -1

        return 1

    @CoreContext.requires_storage
    def delete_experiment(self, experiment_name):
        try:
            self.storage.experiments.delete({"$eq":experiment_name})
        except:
            return -1
        return 1

    def initialize_storage(self, storage_name):
        filename = "{}.quark".format(storage_name)
        self.create_storage(filename)


class ExperimentContext(CoreContext):
    def __init__(self, directory, context_initializer):
        super().__init__(directory, context_initializer)

    @property
    def params(self):
        return self.storage.params.to_dict()

    @property
    def pipeline(self):
        return self.storage.pipeline.to_dict()

    @CoreContext.requires_storage
    def add_script(self, stage, script_name):
        try:
            scripts = self.storage.pipeline.get(stage)
            scripts.append(script_name)
            self.storage.pipeline.set(stage, scripts)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def remove_script(self, stage, script_name):
        try:
            scripts = self.storage.pipeline.get(stage)
            scripts.remove(script_name)
            self.storage.pipeline.set(stage, scripts)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def remove_stage(self, stage):
        try:
            self.storage.pipeline.delete(stage)
        except:
            return -1
        return 1

    @CoreContext.requires_storage
    def add_parameter(self, name, value):
        return self.storage.params.set(name, value)

    @CoreContext.requires_storage
    def remove_parameter(self, name):
        return self.storage.params.delete(name)
