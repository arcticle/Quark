from fnmatch import fnmatch
from future.utils import viewitems
from quark.storage.query_selector import selectors


class QueryCommand(object):
    def __init__(self, query_criteria):
        
        self.query_handlers = {
            dict  : self._query_dict,
            int   : self._query_numeric,
            float : self._query_numeric,
            str   : self._query_string
        }
        self.query = Query(query_criteria)

    def execute(self, data):
        query_handler = self.query_handlers[type(data)]
        return query_handler(data)

        if not isinstance(data, dict):
            raise ValueError("Invalid query operation. " + 
                "Query commands can't be executed on '{}' type".format(type(data).__name__))


    def _query_dict(self, data):
        for query_operator in self.query.query_operators:
            if query_operator(data) == False:
                return False
        return True

    def _query_numeric(self, data):
        for query_operator in self.query.query_operators:
            return query_operator(data)

    def _query_string(self, data):
        for query_operator in self.query.query_operators:
            return query_operator(data)


class Query(object):
    def __init__(self, query_criteria):
        self.query_operators = []
        self._parse_query(query_criteria)

    def _parse_query(self, query):
        if not isinstance(query, dict):
            raise ValueError("Invalid query object specified." +
                "Query object should be of type 'dict' not '{}'".format(type(query).__name__))

        for field, filter in viewitems(query):
            if field in selectors.operators:
                selector_name = field
                field_name    = None
                filter_value  = filter
            else:
                selector_name, filter_value = self._parse_filter(filter)
                field_name = field

            self.query_operators.append(
                self._query_operator(selectors.get(selector_name),
                                    field_name,
                                    filter_value))

    def _parse_filter(self, filter):
        if isinstance(filter, dict):
            selector_name   = next(iter(filter))
            filter_value    = filter[selector_name]
        else:
            selector_name   = "$eq"
            filter_value    = filter
        return selector_name, filter_value

    def _query_operator(self, selector, field, filter_value):
        def call(data):
            if field is None:
                actual_value = data
            else:
                actual_value = data[field]
            return selector(actual_value, filter_value)
        return call


