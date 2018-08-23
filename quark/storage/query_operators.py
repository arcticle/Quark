from fnmatch import fnmatch
from future.builtins import super


class QuerySelector(dict):
    def __init__(self):
        super().__init__()

    def add(self, operator):
        def add_wrapper(operator_function):
            self[operator] = operator_function()
        return add_wrapper

    def get(self, operator):
        return self[operator]

    def str(self, actual, expected):
        return fnmatch(actual, expected)


operators = QuerySelector()

@operators.add("$eq")
def eq():
    return "=="

@operators.add("$gt")
def gt():
    return ">"
    
@operators.add("$lt")
def lt():
    return "<"

@operators.add("$gte")
def gte():
    return ">="

@operators.add("$lte")
def lte():
    return "<="

@operators.add("$in")
def in_():
    return "in"

@operators.add("$str")
def str_():
    def str_func(field, value):
        return "operators.str('{}','{}')".format(field, value) 
    return str_func

# @selectors.add("$eq")
# def eq(actual, excpected):
#     return actual == excpected

# @selectors.add("$gt")
# def gt(actual, excpected):
#     return actual > excpected
    
# @selectors.add("$lt")
# def lt(actual, excpected):
#     return actual < excpected

# @selectors.add("$gte")
# def gte(actual, excpected):
#     return actual >= excpected

# @selectors.add("$lte")
# def lte(actual, excpected):
#     return actual <= excpected

# @selectors.add("$in")
# def in_(actual, excpected):
#     return actual in excpected

# @selectors.add("$str")
# def str_(actual, excpected):
#     return fnmatch(actual, excpected)
