from future.builtins import super


class CollectionItemNotFoundException(Exception):
    pass

class InvalidExpressionException(Exception):
    def __init__(self, exp, data):
        super().__init__(
            "Specified query expression '{}' is not relevant to data type '{}'"
                .format(str(exp), type(data).__name__))


class StorageObjectException(Exception):
    def __init__(self, obj, action, inner_exception):
        super().__init__(
            "Error occured during '{}' action on storage '{}'. ".format(action, obj) +
                "Reason: {}".format(inner_exception)
        )