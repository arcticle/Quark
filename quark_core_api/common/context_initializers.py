from quark_core_api.common import object_initializers as initializers
from quark_core_api.common import schemas


class ContextInitializer(object):
    null = None
    def __init__(self, object_initializer, schema):
        self.object_initializer = object_initializer
        self.schema = schema

    @staticmethod
    def create(object_initializer, schema):
        return ContextInitializer(object_initializer, schema)

    null        = None
    application = None
    workspace   = None
    experiment  = None


ContextInitializer.null        = ContextInitializer.create(None, None)
ContextInitializer.application = ContextInitializer.create(initializers.APPLICATION, schemas.APPLICATION_SCHEMA)
ContextInitializer.workspace   = ContextInitializer.create(initializers.WORKSPACE, None)
ContextInitializer.experiment  = ContextInitializer.create(initializers.EXPERIMENT, None)