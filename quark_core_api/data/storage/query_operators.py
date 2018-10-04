from fnmatch import fnmatch
from functools import wraps
from future.builtins import super
from future.utils import viewitems

class QueryOperators(object):
    
    _operators = {
        "logical"    : {},
        "comparison" : {},
        "evaluation" : {}
    }

    @staticmethod
    def add(operator):
        @wraps(operator)
        def add_wrapper(operator_function):
            return operator, operator_function
        return add_wrapper

    @staticmethod
    def logical_operator(operator_func):
        def wrapper(operator_func):
            op = operator_func[0]
            func = operator_func[1]
            QueryOperators._operators["logical"][op] = func
        return wrapper(operator_func)

    @staticmethod
    def comparison_operator(operator_func):
        def wrapper(operator_func):
            op = operator_func[0]
            func = operator_func[1]
            QueryOperators._operators["comparison"][op] = func
        return wrapper(operator_func)


    @staticmethod
    def evaluation_operator(operator_func):
        def wrapper(operator_func):
            op = operator_func[0]
            func = operator_func[1]
            QueryOperators._operators["evaluation"][op] = func
        return wrapper(operator_func)
    
    @staticmethod
    def has(operator):
        for operator_group in QueryOperators._operators:
            if operator in QueryOperators._operators[operator_group]:
                return True
        return False

    @staticmethod
    def get(operator):
        for op_dict in QueryOperators._iter():
            for op, func in viewitems(op_dict):
                if op == operator:
                    return func 

    @staticmethod
    def _iter():
        for operator_group in QueryOperators._operators:
            yield QueryOperators._operators[operator_group]



    logical    = _operators["logical"]
    comparison = _operators["comparison"]
    evaluation = _operators["evaluation"]





# Comparison query operators
@QueryOperators.comparison_operator
@QueryOperators.add("$eq")
def eq(left, right):
    return left == right

@QueryOperators.comparison_operator
@QueryOperators.add("$gt")
def gt(left, right):
    return left > right

@QueryOperators.comparison_operator
@QueryOperators.add("$lt")
def lt(left, right):
    return left < right

@QueryOperators.comparison_operator
@QueryOperators.add("$gte")
def gte(left, right):
    return left >= right

@QueryOperators.comparison_operator
@QueryOperators.add("$lte")
def lte(left, right):
    return left <= right

@QueryOperators.comparison_operator
@QueryOperators.add("$in")
def in_(left, right):
    return left in right


# Logical query operators
@QueryOperators.logical_operator
@QueryOperators.add("$and")
def and_(left, right):
    return left and right

@QueryOperators.logical_operator
@QueryOperators.add("$or")
def or_(left, right):
    return left or right

@QueryOperators.logical_operator
@QueryOperators.add("$not")
def not_(left, right):
    return left != right


# Evaluation query operators
@QueryOperators.evaluation_operator
@QueryOperators.add("$str")
def str_(left, right):
    return fnmatch(left, right)



class LogicalOperator(object):
    AND = "$and"
    OR  = "$or"
    IS  = "$is"
    NOT = "$not"


