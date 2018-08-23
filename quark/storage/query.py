from fnmatch import fnmatch
from future.utils import viewitems
from quark.storage.query_operators import operators


class QueryCommand(object):
    def __init__(self, query):
        self.query = Query(query)

    def execute(self, data):
        exp = self.query.filter.compile(data)
        return eval(exp)


        if not isinstance(data, dict):
            raise ValueError("Invalid query operation. " + 
                "Query commands can't be executed on '{}' type".format(type(data).__name__))


    # def _query_dict(self, data):
    #     for query_filter in self.query.filters:
    #         if query_filter(data) == False:
    #             return False
    #     return True

    # def _query_numeric(self, data):
    #     for query_filter in self.query.filters:
    #         return query_filter(data)

    # def _query_string(self, data):
    #     for query_filter in self.query.filters:
    #         return query_filter(data)




class ConditionExpression(object):
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

    def compile(self, data):
        field_value = data

        if self.field:
            field_value = data[self.field]

        exp = self.operator(field_value, self.value)

        return exp


class FilterExpression(object):
    def __init__(self):
        self.filters = []
        self.conditions = []

    def add_condition(self, field, operator, value):
        self.conditions.append(
            ConditionExpression(field, operator, value))
    
    def add_filter(self, logical_operator):
        exp = FilterExpression()
        self.filters.append((logical_operator, exp))
        return exp

    def compile(self, data):
        for index, condition in enumerate(self.conditions):
            if index == 0:
                exp = condition.compile(data)
                continue
            exp += " {} {}".format("and", condition.compile(data))
        
        exp = "({})".format(exp)

        for f in self.filters:
            exp += " {} {}".format(f[0], f[1].compile(data))
        
        if len(self.filters) > 0:
            exp = "({})".format(exp)

        return exp


class Query(object):
    def __init__(self, query_filter):
        self.filter = None
        self.fields = set()
        self._build(query_filter)

    def _build(self, query_filter):
        if not isinstance(query_filter, dict):
            raise ValueError("Invalid query filter provided." +
                "Query filter should be of type 'dict' not '{}'".format(type(query_filter).__name__))        

        self.filter = FilterExpression()

        for key, value in viewitems(query_filter):
            if key in operators:
                self.filter.add_condition(None, operators[key], value)
                self.fields.add(None)
            else:
                operator, filter_value = self._parse_filter(value)
                self.filter.add_condition(key, operators[operator], filter_value)
                self.fields.add(key)

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


