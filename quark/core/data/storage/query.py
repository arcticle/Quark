from future.utils import viewitems
from quark.core.data.storage import QueryOperators, LogicalOperator
from quark.exceptions.storage_exceptions import InvalidExpressionException



class QueryCommand(object):
    def __init__(self, query):
        self.query = Query(query)

    def execute(self, data):
        return self.query.filter(data)




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
        exp = ConditionExpression(field, operator, value)
        self.conditions.append(exp)
    
    def add_filter(self, filter_expression):
        self.filters.append(filter_expression)

    def __call__(self, data):
        def collect(expressions):
       
            result = None

            for expression in expressions:
                if result is None:
                    result = expression(data)
                else:
                    right = expression(data)
                    result = self.filter_operator(result, right)

            return result

        exp = None

        if len(self.conditions) > 0:
            exp = collect(self.conditions)

        if len(self.filters) > 0:
            exp = self.filter_operator(exp, collect(self.filters))

        return exp

class Query(object):
    def __init__(self, query_filter):
        self.filter = None
        self._build(query_filter)

    def _build(self, query_filter):
        if not isinstance(query_filter, dict):
            raise ValueError("Invalid query filter provided." +
                "Query filter should be of type 'dict' not '{}'".format(type(query_filter).__name__))        

        self.filter = FilterExpression(QueryOperators.logical[LogicalOperator.AND])

        for key, value in viewitems(query_filter):
            if key in QueryOperators.logical:
                self.filter = FilterExpression(QueryOperators.logical[key])
                for field, operator, filter_value in self._parse_logical_filter(value):
                    self.filter.add_condition(field, QueryOperators.get(operator), filter_value)
                continue

            if QueryOperators.has(key):
                self.filter.add_condition(None, QueryOperators.get(key), value)
            else:
                operator, filter_value = self._parse_filter(value)
                self.filter.add_condition(key, QueryOperators.get(operator), filter_value)

    def _parse_filter(self, filter):
        if isinstance(filter, dict):
            selector_name   = next(iter(filter))
            filter_value    = filter[selector_name]
        else:
            selector_name   = "$eq"
            filter_value    = filter
        return selector_name, filter_value

    def _parse_logical_filter(self, filter):
        if isinstance(filter, dict):
            for key, value in viewitems(filter):
                operator, filter_value = self._parse_filter(value)
                yield key, operator, filter_value

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


