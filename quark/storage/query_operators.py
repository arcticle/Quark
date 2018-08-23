from fnmatch import fnmatch
from future.builtins import super


class QuerySelector(dict):
    def __init__(self):
        super().__init__()

    def add(self, operator):
        def add_wrapper(operator_function):
            self[operator] = operator_function
        return add_wrapper

    def get(self, operator):
        return self[operator]

    def str(self, actual, expected):
        return fnmatch(actual, expected)


operators = QuerySelector()

@operators.add("$eq")
def eq(left, right):
    return left == right

@operators.add("$gt")
def gt(left, right):
    return left > right
    
@operators.add("$lt")
def lt(left, right):
    return left < right

@operators.add("$gte")
def gte(left, right):
    return left >= right

@operators.add("$lte")
def lte(left, right):
    return left <= right

@operators.add("$in")
def in_(left, right):
    return left in right

@operators.add("$str")
def str_(left, right):
    return fnmatch(left, right)



class LogicalOperator(object):
    AND = "and"
    OR  = "or"
    IS  = "is"
    NOT = "not"




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
