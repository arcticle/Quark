import unittest
from quark.storage.query_operators import operators

class TestQuerySelector(unittest.TestCase):
    def setUp(self):
        self._operators = {
            "$eq" : "==",
            "$gt" : ">",
            "$lt" : "<",
            "$gte": ">=",
            "$lte": "<=",
            "$in" : "in"}

    def test_operator_eq(self):
        _operator = operators["$eq"]
        assert _operator == self._operators["$eq"]

    def test_operator_gt(self):
        _operator = operators["$gt"]
        assert _operator == self._operators["$gt"]

    def test_operator_lt(self):
        _operator = operators["$lt"]
        assert _operator == self._operators["$lt"]

    def test_operator_gte(self):
        _operator = operators["$gte"]
        assert _operator == self._operators["$gte"]

    def test_operator_lte(self):
        _operator = operators["$lte"]
        assert _operator == self._operators["$lte"]

    def test_operator_in(self):
        _operator = operators["$in"]
        assert _operator == self._operators["$in"]

    def test_operator_str(self):
        operator_function = operators["$str"]
        assert operator_function("field","*w?ldcard*") == "operators.str('field','*w?ldcard*')"