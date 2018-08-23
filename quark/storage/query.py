from future.utils import viewitems
from quark.storage.query_operators import operators, LogicalOperator
from quark.exceptions.storage_exceptions import InvalidExpressionException



class QueryCommand(object):
    def __init__(self, query):
        self.query = Query(query)

    def execute(self, data):
        exp = self.query.filter(data)
        return eval(exp)


class ConditionExpression(object):
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

    def __call__(self, data):
        field_value = data

        if self.field:
            if not isinstance(data, dict):
                raise InvalidExpressionException(self.field, data)

            field_value = data[self.field]

        return self.operator(field_value, self.value)


class FilterExpression(object):
    def __init__(self, logical_operator):
        self.filter_operator = logical_operator
        self.filters = []
        self.conditions = []

    def add_condition(self, field, operator, value):
        self.conditions.append(
            ConditionExpression(field, operator, value))
    
    def add_filter(self, filter_expression):
        self.filters.append(filter_expression)

    def __call__(self, data):
        def collect(expressions):
            for idx, expr in enumerate(expressions):
                if idx == 0:
                    ex = str(expr(data))
                    continue

                ex += " {} {}".format(
                    self.filter_operator, str(expr(data)))
            return ex
        
        exp = None

        if len(self.conditions) > 0:
            exp = collect(self.conditions)

        if len(self.filters) > 0 and exp:
            return "({} {} {})".format(
                exp, self.filter_operator, collect(self.filters))

        if exp:
            return "({})".format(exp)

class Query(object):
    def __init__(self, query_filter):
        self.filter = None
        self._build(query_filter)

    def _build(self, query_filter):
        if not isinstance(query_filter, dict):
            raise ValueError("Invalid query filter provided." +
                "Query filter should be of type 'dict' not '{}'".format(type(query_filter).__name__))        

        self.filter = FilterExpression(LogicalOperator.AND)

        for key, value in viewitems(query_filter):
            if key in operators:
                self.filter.add_condition(None, operators[key], value)
            else:
                operator, filter_value = self._parse_filter(value)
                self.filter.add_condition(key, operators[operator], filter_value)

    # def _build_filters(self, query_filter):
    #     if not isinstance(query_filter, dict):
    #         raise ValueError("Invalid query filter provided." +
    #             "Query filter should be of type 'dict' not '{}'".format(type(query_filter).__name__))

    #     for field, filter in viewitems(query_filter):
    #         if field in selectors.operators:
    #             self.filters.append(
    #                 self._equality_filter(filter, field))
    #         else:
    #             operator, filter_value = self._parse_filter(filter)
    #             self.filters.append(
    #                 self._conditional_filter(field, filter_value, operator))


    def _parse_filter(self, filter):
        if isinstance(filter, dict):
            selector_name   = next(iter(filter))
            filter_value    = filter[selector_name]
        else:
            selector_name   = "$eq"
            filter_value    = filter
        return selector_name, filter_value

    # def _query_operator(self, selector, field, filter_value):
    #     def call(data):
    #         if field is None:
    #             actual_value = data
    #         else:
    #             actual_value = data[field]
    #         return selector(actual_value, filter_value)
    #     return call

    # def _equality_filter(self, filter_value, operator):
    #     selector = self._query_selector.get(operator)
        
    #     def func(data):
    #         return selector(data, filter_value)
        
    #     return func

    # def _conditional_filter(self, field, filter_value, operator):
    #     selector = self._query_selector.get(operator)

    #     def func(data):
    #         return selector(data[field], filter_value)
        
    #     return func


