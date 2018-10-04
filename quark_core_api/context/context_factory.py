from quark_core_api.context import CoreContext



class CoreContextFactory(object):
    def __init__(self):
        self._types = {}

        for ct in CoreContext.__subclasses__():
            self._types[ct.__name__] = ct

    def create(self, context_type):
        if context_type in self._types:
            context = self._types[context_type]
            return context()
