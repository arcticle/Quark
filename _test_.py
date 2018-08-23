# import copy
# from quark.storage import StorageObjectFactory, Storage



# data = {
#     "repositories": [
#         {"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
#         {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"},
#         {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}
#     ],

#     "user": {"name":"John Doe", "email":"john@doe.com"},

#     "repo_limit" : 10,

#     "tags" : [
#         "Data Analytics 101",
#         "Artificial Intelligence",
#         "Arcticle",
#         "Quark"
#     ],

#     "scores" : [100, 200, 300, 400]
# }






# storage = Storage(copy.deepcopy(data), StorageObjectFactory())
# storage.repositories.update({"name":{"$in":["Repo-2","Repo-3"]}}, {"dir":"Updated", "name":"Repo-Updated"})

from quark.storage.query_operators import operators, LogicalOperator


class QueryExpression(object):
    def __init__(self, filter_expression):
        self.criteria = filter_expression

    def __call__(self, data):
        exp = self.criteria(data)
        return eval(exp)

class ConditionExpression(object):
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

    def __call__(self, data):
        field_value = data

        if self.field:
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

d = {"a":1, "b":2}

f1 = FilterExpression(LogicalOperator.OR)
f1.add_condition("a", operators["$gt"], 5)
f1.add_condition("b", operators["$lt"], 5)

f2 = FilterExpression(LogicalOperator.OR)
f2.add_condition("a", operators["$gte"], 3)
f2.add_condition("b", operators["$lte"], 3)

f1.add_filter(f2)

print(QueryExpression(f1)(d))