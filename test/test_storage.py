import pytest
import copy
import unittest
from quark_core_api.data.storage import InMemoryStorage, StorageObjectFactory


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

schema = {
    "repositories": {
        "$required" : ["id", "name", "dir"],
        "$unique"   : ["id", "name", "dir"],
        "$fields"   : {
            "id" : {
                "$type" : int
            },
            "name" : {
                "$type" : str
            },
            "dir" : {
                "$type" : str
            }
        }
    }
}

storage = InMemoryStorage("test_storage", data)


def test_keyvalueobject_get_value():
    assert storage.repo_limit.value == 10

def test_keyvalueobject_get_value_using_indexer():
    assert storage["repo_limit"].value == 10

def test_keyvalueobject_set_value():
    storage.repo_limit.value = 20
    assert storage.repo_limit.value == 20

def test_keyvalueobject_set_value_using_indexer():
    storage["repo_limit"].value = 20
    assert storage.repo_limit.value == 20

def test_complexobject_get_value():
    assert storage.user.get("name") == "John Doe"
    assert storage.user.get("email") == "john@doe.com"

def test_complexobject_get_value_by_attribute():
    assert storage.user.name == "John Doe"
    assert storage.user.email == "john@doe.com"

def test_complexobject_set_value():
    storage = InMemoryStorage("test_storage", data)
    storage.user.set("name","Foo Bar")
    storage.user.set("email","foo@bar.com")
    assert storage.user.name == "Foo Bar"
    assert storage.user.email == "foo@bar.com"


def test_complexobject_set_value_by_attribute():
    storage.user.name = "Foo Bar"
    storage.user.email = "foo@bar.com"
    assert storage.user.name == "Foo Bar"
    assert storage.user.email == "foo@bar.com"


def test_collectionobject_simpletype_eq_query_case1():
    result = storage.scores.find({"$eq":100})
    assert result == [100]

def test_collectionobject_simpletype_eq_query_case2():
    result = storage.scores.find({"$eq":1000})
    assert result == []

def test_collectionobject_simpletype_gt_query_case1():
    result = storage.scores.find({"$gt":200})
    assert result == [300,400]

def test_collectionobject_simpletype_gt_query_case2():
    result = storage.scores.find({"$gt":400})
    assert result == []

def test_collectionobject_simpletype_gt_query_findone():
    result = storage.scores.find_one({"$gt":200})
    assert result == 300

def test_collectionobject_simpletype_gte_query_case1():
    result = storage.scores.find({"$gte":200})
    assert result == [200,300,400]

def test_collectionobject_simpletype_gte_query_case2():
    result = storage.scores.find({"$gte":500})
    assert result == []

def test_collectionobject_simpletype_gte_query_findone():
    result = storage.scores.find_one({"$gte":400})
    assert result == 400

def test_collectionobject_simpletype_lt_query_case1():
    result = storage.scores.find({"$lt":300})
    assert result == [100,200]

def test_collectionobject_simpletype_lt_query_case2():
    result = storage.scores.find({"$lt":100})
    assert result == []

def test_collectionobject_simpletype_lte_query_case1():
    result = storage.scores.find({"$lte":300})
    assert result == [100,200,300]

def test_collectionobject_simpletype_lte_query_case2():
    result = storage.scores.find({"$lte":50})
    assert result == []

def test_collectionobject_simpletype_str_query_case1():
    result = storage.tags.find({"$str":"*101*"})
    assert result == ["Data Analytics 101"]

def test_collectionobject_simpletype_str_query_case2():
    result = storage.tags.find({"$str":"*t?c*"})
    assert result == ["Data Analytics 101", "Arcticle"]

def test_collectionobject_simpletype_in_query_case1():
    result = storage.tags.find({"$in":["Quark", "AI"]})
    assert result == ["Quark"]

def test_collectionobject_simpletype_in_query_case2():
    result = storage.tags.find({"$in":["Arcticle Labs", "AI"]})
    assert result == []

def test_collectionobject_simpletype_in_query_case3():
    result = storage.tags.find({"$in":[1,2,3]})
    assert result == []

def test_collectionobject_simpletype_in_query_case4():
    result = storage.tags.find({"$in":[]})
    assert result == []

def test_collectionobject_simpletype_in_query_case5():
    result = storage.scores.find({"$in":[100,200,300,1000,2000]})
    assert result == [100,200,300]

def test_collectionobject_simpletype_in_query_case6():
    result = storage.scores.find({"$in":[1000,2000]})
    assert result == []

def test_collectionobject_complextype_query_case1():
    result = storage.repositories.find({"id":2})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}]


def test_collectionobject_complextype_query_case2():
    result = storage.repositories.find({"id":{"$eq":2}})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}]

def test_collectionobject_complextype_query_case3():
    result = storage.repositories.find({"id":{"$gt":2}})
    assert result == [{"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_complextype_query_case4():
    result = storage.repositories.find({"id":{"$gte":2}})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}, 
                    {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_complextype_query_case5():
    result = storage.repositories.find({"name":{"$str":"Repo*"}})
    assert result == [{"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
                    {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}, 
                    {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]

def test_collectionobject_complextype_query_case6():
    result = storage.repositories.find({"id":2, "name":"Repo-2"})
    assert result == [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"}]

def test_collectionobject_complextype_query_case7():
    result = storage.repositories.find({"$or": {"id":2, "name":"Repo-3"}})
    expected = [{"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"},
                {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}]
    assert all([True if o in result else False for o in expected]) and len(result) == len(expected)


def test_collectionobject_simpletype_update_case1():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.scores.update({"$eq":100}, 101)
    assert storage.data["scores"][0] == 101

def test_collectionobject_simpletype_update_case2():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.scores.update({"$gt":100}, 1111)
    assert storage.data["scores"] == [100,1111,1111,1111]

def test_collectionobject_simpletype_update_case3():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.tags.update({"$str":"*tic*"}, "Updated")
    assert storage.data["tags"] == ["Updated","Artificial Intelligence","Updated","Quark"]

def test_collectionobject_complextype_update_case1():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.repositories.update({"name":{"$in":["Repo-2","Repo-5"]}}, {"dir":"Updated"})
    assert storage.data["repositories"][1]["dir"] == "Updated"

def test_collectionobject_complextype_update_case2():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.repositories.update({"name":{"$in":["Repo-2","Repo-3"]}}, {"dir":"Updated", "name":"Repo-Updated"})
    assert storage.data["repositories"][1]["name"] == "Repo-Updated"
    assert storage.data["repositories"][2]["name"] == "Repo-Updated"
    assert storage.data["repositories"][1]["dir"] == "Updated"
    assert storage.data["repositories"][2]["dir"] == "Updated"

def test_collectionobject_complextype_insert_case1():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.repositories.insert({"id":4, "name":"Repo-4", "dir":"c:/repos/repo4"})
    assert storage.data["repositories"][3] == {"id":4, "name":"Repo-4", "dir":"c:/repos/repo4"}

def test_collectionobject_simpletype_insert_case1():
    storage = InMemoryStorage("test_storage", copy.deepcopy(data))
    storage.tags.insert("New Tag")
    assert storage.data["tags"] == ["Data Analytics 101","Artificial Intelligence","Arcticle","Quark", "New Tag"]

def test_collectionobject_complextype_invalid_query():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    with pytest.raises(StorageObjectException):
        result = storage.tags.find({"id":{"$gt":2}})

def test_collectionobject_complextype_insert_id_uniqueness_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":2, "name":"Repo-4", "dir":"c:/repos/repo4"})
    except StorageObjectException as se:
        assert "Uniqueness validation" in str(se)

def test_collectionobject_complextype_insert_name_uniqueness_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":4, "name":"Repo-2", "dir":"c:/repos/repo4"})
    except StorageObjectException as se:
        assert "Uniqueness validation" in str(se)

def test_collectionobject_complextype_insert_dir_uniqueness_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":4, "name":"Repo-4", "dir":"c:/repos/repo2"})
    except StorageObjectException as se:
        assert "Uniqueness validation" in str(se)

def test_collectionobject_complextype_insert_uniqueness_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"})
    except StorageObjectException as se:
        assert "Uniqueness validation" in str(se)

def test_collectionobject_complextype_insert_required_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":4, "name":"Repo-2"})
    except StorageObjectException as se:
        assert "Required validation" in str(se)

def test_collectionobject_complextype_insert_type_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    try:
        storage.repositories.insert({"id":"abc", "name":"Repo-4", "dir":"c:/repos/repo4"})
    except StorageObjectException as se:
        assert "Type validation" in str(se)

def test_collectionobject_complextype_insert_no_validation_error():
    from quark_core_api.exceptions.storage_exceptions import StorageObjectException
    storage = InMemoryStorage("test_storage", copy.deepcopy(data), schema)
    storage.repositories.insert({"id":4, "name":"Repo-4", "dir":"c:/repos/repo4"})