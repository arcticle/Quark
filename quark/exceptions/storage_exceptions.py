from future.builtins import super


class CollectionItemNotFoundException(Exception):
    pass

class InvalidExpressionException(Exception):
    def __init__(self, exp, data):
        super().__init__(
            "Specified query expression '{}' is not relevant to data type '{}'"
                .format(str(exp), type(data).__name__))