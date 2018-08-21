from fnmatch import fnmatch
from future.utils import viewitems



class QueryCommand(object):
    def __init__(self, query):
        
        self.selectors = {
            "$eq"  : QuerySelector.eq,
            "$gt"  : QuerySelector.gt,
            "$lt"  : QuerySelector.lt,
            "$gte" : QuerySelector.gte,
            "$lte" : QuerySelector.lte,
            "$in"  : QuerySelector.in_,
            "$str" : QuerySelector.str_
        }

        self.query_handlers = {
            dict  : self._query_dict,
            int   : self._query_numeric,
            float : self._query_numeric,
            str   : self._query_string
        }
        self.query = query

    def execute(self, data):
        query_handler = self.query_handlers[type(data)]
        return query_handler(data)

        if not isinstance(data, dict):
            raise ValueError("Invalid query operation. " + 
                "Query commands can't be executed on '{}' type".format(type(data).__name__))


    def _query_dict(self, data):
        for field, filter in viewitems(self.query):
            selector, value = self._parse_filter(filter)
            if selector(data[field], value) == False:
                return False
        return True

    def _query_numeric(self, data):
        selector, value = self._parse_filter(self.query)
        return selector(data, value)

    def _query_string(self, data):
        selector, value = self._parse_filter(self.query)
        if selector.__name__ != "str_":
            raise ValueError("Invalid query operation. " + 
                "'{}' selectors can't be executed on 'str' type".format(selector))
        return selector(data, value)


    def _parse_filter(self, filter):
        if isinstance(filter, dict):
            selector = next(iter(filter))
            value    = filter[selector]
        else:
            selector = "$eq"
            value    = filter
        return self.selectors[selector], value


class QuerySelector(object):

    @staticmethod
    def eq(actual, excpected):
        return actual == excpected

    @staticmethod
    def gt(actual, excpected):
        return actual > excpected
        
    @staticmethod
    def lt(actual, excpected):
        return actual < excpected

    @staticmethod
    def gte(actual, excpected):
        return actual >= excpected

    @staticmethod
    def lte(actual, excpected):
        return actual <= excpected

    @staticmethod
    def in_(actual, excpected):
        return actual in excpected

    @staticmethod
    def str_(actual, excpected):
        return fnmatch(actual, excpected)
