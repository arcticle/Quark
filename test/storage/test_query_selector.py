import pytest
from quark.storage.query_operators import operators


testcases = [
    ("$eq" , 1, 2 , "1 == 2"),
    ("$gt" , 1, 2 , "1 > 2" ),
    ("$lt" , 1, 2 , "1 < 2" ),
    ("$gte", 1, 2 , "1 >= 2"),
    ("$lte", 1, 2 , "1 <= 2"),
    ("$in" , 1, 2 , "1 in 2"),
    ("$str", "foo","*f?o*","operators.str('foo','*f?o*')"),
]

@pytest.mark.parametrize("operator,left,right,expected", testcases)
def test_operator_functions(operator, left, right, expected):
    assert operators[operator](left, right) == expected


