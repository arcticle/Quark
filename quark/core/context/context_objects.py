import os
from datetime import datetime
from future.utils import viewitems
from collections.abc import Mapping
from quark.core.context import ApplicationContext, WorkspaceContext, ExperimentContext



class Application(object):
    def __init__(self):
        self._context = ApplicationContext()
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
            ws = Workspace(ws_id, name, ws_dir)
            self._workspaces[result] = ws
            return ws

    def delete_workspace(self, id):
        result = self._context.delete_workspace(int(id))

        if result > 0:
            del self._workspaces[id]


    def __initialize__(self):
        for ws in self._context.workspaces:
            self._workspaces[ws["id"]] = Workspace(**ws)



class Workspace(object):
    def __init__(self, id, name, dir):
        
        self._id = id
        self._name = name
        self._directory = dir
        self._experiments = {}
        self._scripts = {}
        
        self._context = WorkspaceContext(name, dir)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def directory(self):
        return self._directory

    @property
    def experiments(self):
        return self._experiments

    @property
    def scripts(self):
        return self._scripts.values()


    def create_experiment(self, name):
        xp_dir = os.path.join(self._directory, "experiments", name)
        result = self._context.create_experiment(name)

        if result > 0:
            xp = Experiment(name, xp_dir, self._scripts)
            self._experiments[name] = xp
            return xp

    def delete_experiment(self, name):
        result = self._context.delete_experiment(name)

        if result > 0:
            del self._experiments[name]

    def create_script(self, script_name, content):
        result = self._context.create_script(script_name, content)

        if result > 0:
            scr = Script(script_name, "")
            self._scripts[script_name] = scr
            return scr

class Experiment(object):
    def __init__(self, name, dir, scripts):
        self._name = name
        self._directory = dir
        self._scripts = scripts

        self._context = ExperimentContext(name, dir)

        self._pipeline = self._create_pipeline()

    def add_script(self, script):
        result = self._context.add_script(script)

        if result > 0:
            self._pipeline.add_step(self._scripts[script])

    def add_parameter(self, name, value):
        result = self._context.add_parameter(name, value)

        if result > 0:
            self._pipeline.add_param(name, value)

    def _create_pipeline(self):
        scripts = [] 
        for script in self._context.pipeline:
            if script in self._scripts:
                scripts.append(self._scripts[script])

        steps = tuple(scripts)
        return Pipeline(*steps, params=self._context.params)


class Script(object):
    def __init__(self, alias, filename):
        self._alias = alias
        self._filename = filename

    @property
    def name(self):
        return self._alias



class Pipeline(Mapping):
    def __init__(self, *args, **kw):
        self._steps = []
        self._scripts = {}
        self._params = {}

        if args:
            for script in args:
                self.__addstep__(script.name, script)

        if kw:
            for name, value in viewitems(kw):
                if name == "params":
                    self._params = value
                else:
                    self.__addstep__(name, value)

    @property
    def num_of_steps(self):
        return len(self._scripts)

    def add_step(self, script):
        self.__addstep__(script.name, script)

    def add_param(self, name, value):
        self._params[name] = value

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == -1:
                return self._scripts[self.num_of_steps-1]
            return self._scripts[key]
        if isinstance(key, str):
            index = self._steps.index(key)
            return self._scripts[index]

    def __iter__(self):
        for step in range(self.num_of_steps):
            yield self._scripts[step]
    
    def __len__(self):
        return len(self._scripts)

    def __addstep__(self, name, script):
        key = len(self._scripts)
        self._scripts[key] = script
        self._steps.insert(key, name)


