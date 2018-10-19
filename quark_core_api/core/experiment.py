import os
from datetime import datetime
from future.utils import viewitems
from quark_core_api.context import ExperimentContext
from quark_core_api.core import Pipeline
from quark_core_api.exceptions import InvalidContextException, ArgumentException

class QuarkExperiment(object):
    def __init__(self, name, scripts, context):
        if not isinstance(context, ExperimentContext):
            raise InvalidContextException(context)

        self._name = name
        self._scripts = scripts
        self._context = context
        self._pipeline = None

        self.__initialize__()

    @property
    def pipeline(self):
        return self._pipeline

    def add_script(self, stage, script):
        result = self._context.add_script(stage, script)

        if result > 0:
            self._pipeline.add_step(stage, self._scripts[script])

    def add_parameter(self, name, value):
        result = self._context.add_parameter(name, value)

        if result > 0:
            self._pipeline.add_param(name, value)

    def add_parameters(self, params):
        if not isinstance(params, dict):
            raise ArgumentException("params")

        for name, value in viewitems(params):
            self.add_parameter(name, value)

    def __initialize__(self):
        filename = "{}.xpr".format(self._name)
        self._context.create_storage(filename)
        self._pipeline = self._create_pipeline()

    def _create_pipeline(self):
        stages = {}
        if isinstance(self._context.pipeline, list):
            stages["Stage-1"] = self._resolve_scripts(self._context.pipeline)
        elif isinstance(self._context.pipeline, dict):
            for stage, scripts in viewitems(self._context.pipeline):
                stages[stage] = self._resolve_scripts(scripts)

        return Pipeline(**stages, params=self._context.params)

    def _resolve_scripts(self, script_names):
        scripts = []
        for script_name in script_names:
            if script_name in self._scripts:
                scripts.append(self._scripts[script_name])
        return scripts


