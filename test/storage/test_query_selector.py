import pytest
from quark.storage.query_operators import operators


testcases = [
    ("$eq" , 1, 2 , False),
    ("$eq" , 1, 1 , True),
    ("$gt" , 1, 2 , False ),
    ("$gt" , 1, 0 , True ),
    ("$lt" , 1, 0 , False ),
    ("$lt" , 1, 2 , True ),
    ("$gte", 1, 2 , False),
    ("$gte", 1, 1 , True),
    ("$lte", 1, 0 , False),
    ("$lte", 1, 1 , True),
    ("$in" , 1,  [2, 3] , False),
    ("$in" , 1,  [1, 2] , True),
    ("$str", "foo","*foo?",False),
    ("$str", "foo","*f?o*",True),
]

@pytest.mark.parametrize("operator,left,right,expected", testcases)
def test_operator_functions(operator, left, right, expected):
    assert operators[operator](left, right) == expected


