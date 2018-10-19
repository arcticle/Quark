from future.builtins import super


class ArgumentOutOfRangeException(Exception):
    def __init__(self, arg):
        super().__init__(
            "The value of argument '{}' is outside the allowable range of values."
                .format(arg))

class ArgumentException(Exception):
    def __init__(self, arg):
        super().__init__(
            "Provided argument '{}' is not valid."
                .format(arg))

class InvalidOperationException(Exception):
    def __init__(self, exception):
        super().__init__(
            "Performed operation is not valid: '{}'"
                .format(exception))