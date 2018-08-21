import pytest
from quark.storage.query_selector import selectors

operators = [("$eq", "eq"), ("$gt","gt"), ("$lt","lt"), ("$gte","gte"), ("$lte","lte"), ("$in","in_"), ("$str","str_")]

@pytest.fixture(params=operators)
def operator(request):
    return request.param


def test_selector_get(operator):
    selector = selectors.get(operator[0])
    assert selector.__name__ == operator[1]


operations = [
    ("$eq", [(1,1,True), (1,2,False), (2,1,False)]),
    ("$gt", [(1,1,False), (1,2,False), (2,1,True)]),
    ("$lt", [(1,1,False), (1,2,True), (2,1,False)]),
    ("$gte", [(1,1,True), (1,2,False), (2,1,True)]),
    ("$lte", [(1,1,True), (1,2,True), (2,1,False)]),
    ("$in", [(1,[1,2],True), (1,[2,3],False), (1,[],False)]),
    ("$str", [("foobar","*bar",True), ("foobar","f??bar",True), ("foobar","*oo*",True), ("foobar","fo??bar*",False)]),
]

@pytest.fixture(params=operations)
def operation(request):
    return request.param

def test_selector_execute(operation):
    selector = selectors.get(operation[0])
    for left, right, expected in operation[1]:
        assert selector(left, right) == expected
