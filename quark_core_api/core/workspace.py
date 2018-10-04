import os
from quark_core_api.context import WorkspaceContext, ExperimentContext
from quark_core_api.core import QuarkExperiment, Script


class QuarkWorkspace(object):
    def __init__(self, id, name, context):
        if not isinstance(context, WorkspaceContext):
            raise ValueError("Invalid context type has been provided")

        self._id = id
        self._name = name
        self._context = context

        self._experiments = {}
        self._scripts = {}

        self._context.initialize_storage(name)
        self.__initialize__()
        

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def directory(self):
        return self._context.directory

    @property
    def experiments(self):
        return self._experiments

    @property
    def scripts(self):
        return self._scripts.values()


    def create_experiment(self, name):
        result = self._context.create_experiment(name)

        if result > 0:
            xp = self._create_experiment_object(name)
            self._experiments[name] = xp
            return xp

    def delete_experiment(self, name):
        result = self._context.delete_experiment(name)

        if result > 0:
            del self._experiments[name]

    def create_script(self, script_name, content):
        result = self._context.create_script(script_name, content)

        if result > 0:
            scr = self._create_script_object(script_name)
            self._scripts[script_name] = scr
            return scr

    def __initialize__(self):
        for script_name in self._context.scripts:
            self._scripts[script_name] = self._create_script_object(script_name)

        for xp_name in self._context.experiments:
            self._experiments[xp_name] = self._create_experiment_object(xp_name)

    def _get_experiment_location(self, experiment_name):
        return os.path.join(self._context.directory, "experiments", experiment_name)

    def _create_script_object(self, script_name):
        directory = os.path.join(self._context.directory, "scripts")
        return Script(script_name, directory)

    def _create_experiment_object(self, experiment_name):
        xp_dir = self._get_experiment_location(experiment_name)
        args = (experiment_name, self._scripts, ExperimentContext(xp_dir))
        return QuarkExperiment(*args)
