import os, copy
from datetime import datetime
from future.utils import viewitems
from collections.abc import Mapping
from quark.core.context import ApplicationContext, WorkspaceContext, ExperimentContext
from quark.common.utils import Cache


class Application(object):
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
            ws = Workspace(ws_id, name, WorkspaceContext(ws_dir))
            self._workspaces[result] = ws
            return ws

    def delete_workspace(self, id):
        result = self._context.delete_workspace(int(id))

        if result > 0:
            del self._workspaces[id]


    def __initialize__(self):
        for ws in self._context.workspaces:
            args = (ws["id"], ws["name"], WorkspaceContext(ws["dir"]))
            self._workspaces[ws["id"]] = Workspace(*args)



class Workspace(object):
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
        return Experiment(*args)


class Experiment(object):
    def __init__(self, name, scripts, context):
        if not isinstance(context, ExperimentContext):
            raise ValueError("Invalid context type has been provided")

        self._name = name
        self._scripts = scripts
        self._context = context

        self._context.initialize_storage(name)
        self._pipeline = self._create_pipeline()

    @property
    def pipeline(self):
        return self._pipeline

    def add_script(self, script):
        result = self._context.add_script(script)

        if result > 0:
            self._pipeline.add_step(self._scripts[script])

    def add_parameter(self, name, value):
        result = self._context.add_parameter(name, value)

        if result > 0:
            self._pipeline.add_param(name, value)

    def add_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Invalid params object has been provided. " + 
                "Expected \"dict\" but was \"{}\".".format(type(params)))

        for name, value in viewitems(params):
            self.add_parameter(name, value)

    def _create_pipeline(self):
        scripts = [] 
        for script in self._context.pipeline:
            if script in self._scripts:
                scripts.append(self._scripts[script])

        steps = tuple(scripts)
        return Pipeline(*steps, params=self._context.params)


class Script(object):
    def __init__(self, name, directory):
        self._name = name
        self._filename = os.path.join(directory, "{}.py".format(name))

    @property
    def name(self):
        return self._name

    @property
    def filename(self):
        return self._filename

    def run(self, context):
        pass


class Pipeline(object):
    def __init__(self, *args, **kw):
        self._params = {}
        self._cache = Cache()

        if args:
            for script in args:
                self._cache.add(script.name, script)
        if kw:
            for name, value in viewitems(kw):
                if name == "params":
                    self._params = value
                else:
                    self._cache.add(name, value)

    @property
    def params(self):
        return copy.deepcopy(self._params)

    @property
    def steps(self):
        return [value for key, value in self._cache]

    def add_step(self, script):
        self._cache.add(script.name, script)

    def add_param(self, name, value):
        self._params[name] = value

    def __getitem__(self, key):
        return self._cache.get(key)

    def __iter__(self):
        return self._cache.__iter__()
    
    def __len__(self):
        return len(self._cache)


