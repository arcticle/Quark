from future.utils import viewitems




class RepositoryFactory(object):

    @staticmethod
    def create(name, dir, id=None):
        if not id:
            import uuid
            id = uuid.uuid4().hex
        return QuarkRepository(name, dir, id)

    @staticmethod
    def create_from_args(args):
        return QuarkRepository(**args)

class QuarkRepository(object):
    def __init__(self, name=None, dir=None, id=None):
        self.name = name
        self.dir = dir
        self.id = id