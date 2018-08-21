from fnmatch import fnmatch


class QuerySelector(object):
    def __init__(self):
        self.operators = {}

    def add(self, operator):
        def add_wrapper(operator_function):
            self.operators[operator] = operator_function
        return add_wrapper

    def get(self, operator):
        return self.operators[operator]


selectors = QuerySelector()

@selectors.add("$eq")
def eq(actual, excpected):
    return actual == excpected

@selectors.add("$gt")
def gt(actual, excpected):
    return actual > excpected
    
@selectors.add("$lt")
def lt(actual, excpected):
    return actual < excpected

@selectors.add("$gte")
def gte(actual, excpected):
    return actual >= excpected

@selectors.add("$lte")
def lte(actual, excpected):
    return actual <= excpected

@selectors.add("$in_")
def in_(actual, excpected):
    return actual in excpected

@selectors.add("$str_")
def str_(actual, excpected):
    return fnmatch(actual, excpected)