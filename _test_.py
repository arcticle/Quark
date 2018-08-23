import copy
from quark.storage import StorageObjectFactory, Storage



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






storage = Storage(copy.deepcopy(data), StorageObjectFactory())
storage.repositories.update({"name":{"$in":["Repo-2","Repo-3"]}}, {"dir":"Updated", "name":"Repo-Updated"})