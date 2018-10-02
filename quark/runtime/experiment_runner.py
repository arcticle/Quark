from quark.common.utils import Cache, ReadOnlyCache
from quark.core.context.context_objects import Experiment




class RuntimeContext(object):
    def __init__(self, experiment):
        if not isinstance(experiment, Experiment):
            raise Exception("Invalid experiment object has been provided.")

        self._experiment = experiment

    def run_experiment(self):
        pipeline_ctx = PipelineContext(self._experiment.params)
        for script in self._experiment.pipeline:
            script.run(pipeline_ctx)



class PipelineContext(object):
    def __init__(self, params):
        if not isinstance(params, dict):
            raise Exception("Invalid 'params' object type provided.")

        self._params = ReadOnlyCache(**params)
        self._cache = Cache()

    @property
    def params(self):
        return self._params

    @property
    def cache(self):
        return self._cache



