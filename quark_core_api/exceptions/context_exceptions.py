from future.builtins import super



class ContextException(Exception):
    pass

class InvalidContextException(Exception):
    def __init__(self, ctx):
        super().__init__(
            "Invalid context of type '{}' has been provided."
                .format(type(ctx).__name__))