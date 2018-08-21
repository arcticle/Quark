import copy, pytest
from quark.storage import Storage, StorageObjectFactory


data = {
    "repositories": [
        {"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
        {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"},
        {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}
    ],

    "user": {"name":"John Doe", "email":"john@doe.com"},

    "repo_limit" : 10,

    "tags" : [
        "Data Analytics 101",
        "Artificial Intelligence",
        "Arcticle",
        "Quark"
    ],

    "scores" : [100, 200, 300, 400]
}

# storage = Storage(data, StorageObjectFactory())

@pytest.fixture(scope="function", autouse=False)
def storage(request):
    return Storage(data, StorageObjectFactory())

def test_keyvalueobject_get_value(storage):
    assert storage.repo_limit.value == 10

def test_keyvalueobject_set_value(storage):
    storage.repo_limit.value = 20
    assert storage.repo_limit.value == 20

def test_complexobject_get_value(storage):
    assert storage.user.get("name") == "John Doe"
    assert storage.user.get("email") == "john@doe.com"

def test_complexobject_get_value_by_attribute(storage):
    assert storage.user.name == "John Doe"
    assert storage.user.email == "john@doe.com"

def test_complexobject_set_value():
    storage = Storage(data, StorageObjectFactory())
    storage.user.set("name","Foo Bar")
    storage.user.set("email","foo@bar.com")
    assert storage.user.name == "Foo Bar"
    assert storage.user.email == "foo@bar.com"


def test_complexobject_set_value_by_attribute(storage):
    storage.user.name = "Foo Bar"
    storage.user.email = "foo@bar.com"
    assert storage.user.name == "Foo Bar"
    assert storage.user.email == "foo@bar.com"


def test_collectionobject_simpletype_eq_query_case1(storage):
    result = storage.scores.find({"$eq":100})
    assert result == [100]

def test_collectionobject_simpletype_eq_query_case2(storage):
    result = storage.scores.find({"$eq":1000})
    assert result == []

def test_collectionobject_simpletype_gt_query_case1(storage):
    result = storage.scores.find({"$gt":200})
    assert result == [300,400]

def test_collectionobject_simpletype_gt_query_case2(storage):
    result = storage.scores.find({"$gt":400})
    assert result == []

def test_collectionobject_simpletype_gt_query_findone(storage):
    result = storage.scores.find_one({"$gt":200})
    assert result == 300

def test_collectionobject_simpletype_gte_query_case1(storage):
    result = storage.scores.find({"$gte":200})
    assert result == [200,300,400]

def test_collectionobject_simpletype_gte_query_case2(storage):
    result = storage.scores.find({"$gte":500})
    assert result == []

def test_collectionobject_simpletype_gte_query_findone(storage):
    result = storage.scores.find_one({"$gte":400})
    assert result == 400

def test_collectionobject_simpletype_lt_query_case1(storage):
    result = storage.scores.find({"$lt":300})
    assert result == [100,200]

def test_collectionobject_simpletype_lt_query_case2(storage):
    result = storage.scores.find({"$lt":100})
    assert result == []

def test_collectionobject_simpletype_lte_query_case1(storage):
    result = storage.scores.find({"$lte":300})
    assert result == [100,200,300]

def test_collectionobject_simpletype_lte_query_case2(storage):
    result = storage.scores.find({"$lte":50})
    assert result == []

def test_collectionobject_simpletype_str_query_case1(storage):
    result = storage.tags.find({"$str":"*101*"})
    assert result == ["Data Analytics 101"]

def test_collectionobject_simpletype_str_query_case2(storage):
    result = storage.tags.find({"$str":"*t?c*"})
    assert result == ["Data Analytics 101", "Arcticle"]

def test_collectionobject_simpletype_in_query_case1(storage):
    result = storage.tags.find({"$in":["Quark", "AI"]})
    assert result == ["Quark"]

def test_collectionobject_simpletype_in_query_case2(storage):
    result = storage.tags.find({"$in":["Arcticle Labs", "AI"]})
    assert result == []

def test_collectionobject_simpletype_in_query_case3(storage):
    result = storage.tags.find({"$in":[1,2,3]})
    assert result == []

def test_collectionobject_simpletype_in_query_case4(storage):
    result = storage.tags.find({"$in":[]})
    assert result == []

def test_collectionobject_simpletype_in_query_case5(storage):
    result = storage.scores.find({"$in":[100,200,300,1000,2000]})
    assert result == [100,200,300]

def test_collectionobject_simpletype_in_query_case6(storage):
    result = storage.scores.find({"$in":[1000,2000]})
    assert result == []

def test_collectionobject_complextype_query_case1(storage):
    result = storage.repositories.find({"id":2})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}]

def test_collectionobject_complextype_query_case2(storage):
    result = storage.repositories.find({"id":{"$eq":2}})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}]

def test_collectionobject_complextype_query_case3(storage):
    result = storage.repositories.find({"id":{"$gt":2}})
    assert result == [{"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_complextype_query_case4(storage):
    result = storage.repositories.find({"id":{"$gte":2}})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}, 
                      {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_complextype_query_case5(storage):
    result = storage.repositories.find({"name":{"$str":"Repo*"}})
    assert result == [{"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
                      {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}, 
                      {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_simpletype_update_case1():
    storage = Storage(copy.deepcopy(data), StorageObjectFactory())
    storage.scores.update({"$eq":100}, 101)
    assert storage.data["scores"][0] == 101

def test_collectionobject_simpletype_update_case2():
    storage = Storage(copy.deepcopy(data), StorageObjectFactory())
    storage.scores.update({"$gt":100}, 1111)
    assert storage.data["scores"] == [100,1111,1111,1111]

def test_collectionobject_simpletype_update_case3():
    storage = Storage(copy.deepcopy(data), StorageObjectFactory())
    storage.tags.update({"$str":"*tic*"}, "Updated")
    assert storage.data["tags"] == ["Updated","Artificial Intelligence","Updated","Quark"]

def test_collectionobject_complextype_update_case1():
    storage = Storage(copy.deepcopy(data), StorageObjectFactory())
    storage.repositories.update({"name":{"$in":["Repo-2","Repo-5"]}}, {"dir":"Updated"})
    assert storage.data["repositories"][1]["dir"] == "Updated"

def test_collectionobject_complextype_update_case2():
    storage = Storage(copy.deepcopy(data), StorageObjectFactory())
    storage.repositories.update({"name":{"$in":["Repo-2","Repo-3"]}}, {"dir":"Updated", "name":"Repo-Updated"})
    assert storage.data["repositories"][1]["name"] == "Repo-Updated"
    assert storage.data["repositories"][2]["name"] == "Repo-Updated"
    assert storage.data["repositories"][1]["dir"] == "Updated"
    assert storage.data["repositories"][2]["dir"] == "Updated"