from quark.core import context


class QuarkApp(object):
    def __init__(self):
        self.app_context = context.ApplicationContext()





class ContextObject(object):
    def __init__(self, store, context):
        self._store = store
        self._context = context



class Repository(ContextObject):
    def __init__(self):
        pass