import os
from datetime import datetime
from future.utils import viewitems
from quark_core_api.context import ExperimentContext
from quark_core_api.core import Pipeline


class QuarkExperiment(object):
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
