import pytest
from quark_core_api.data.storage.query_operators import QueryOperators


testcases_logical = [
    ("$and", True,  True,  True),
    ("$and", True,  False, False),
    ("$or" , True,  True,  True),
    ("$or" , True,  False, True),
    ("$or" , False, False, False),
    ("$not", 1, 1,  False),
    ("$not", 1, 2,  True)
]


testcases_comparison = [
    ("$eq" , 1, 2 , False),
    ("$eq" , 1, 1 , True),
    ("$gt" , 1, 2 , False),
    ("$gt" , 1, 0 , True),
    ("$lt" , 1, 0 , False),
    ("$lt" , 1, 2 , True),
    ("$gte", 1, 2 , False),
    ("$gte", 1, 1 , True),
    ("$lte", 1, 0 , False),
    ("$lte", 1, 1 , True),
    ("$in" , 1,  [2, 3] , False),
    ("$in" , 1,  [1, 2] , True)
]

testcases_evaluation = [
    ("$str", "foo","*foo?",False),
    ("$str", "foo","*f?o*",True)
]


@pytest.mark.parametrize("operator,left,right,expected", testcases_logical)
def test_logical_operator_function(operator, left, right, expected):
    assert QueryOperators.logical[operator](left, right) == expected


@pytest.mark.parametrize("operator,left,right,expected", testcases_comparison)
def test_comparison_operator_function(operator, left, right, expected):
    assert QueryOperators.comparison[operator](left, right) == expected


@pytest.mark.parametrize("operator,left,right,expected", testcases_evaluation)
def test_evaluation_operator_function(operator, left, right, expected):
    assert QueryOperators.evaluation[operator](left, right) == expected
