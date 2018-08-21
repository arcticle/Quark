from attrdict import AttrDict
from quark.storage import CollectionObject, ComplexObject, KeyValueObject




data = {
    "repositories": [
        {"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
        {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"},
        {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}
    ],

    "user": {"name":"John Doe", "email":"john@doe.com"},

    "repo_limit" : 10,

    "tags" : [
        "Data Analytics",
        "Artificial Intelligence"
    ]
}



class StorageObjectFactory(object):
    def __init__(self, object_types=None):
        self._object_type_map = {}
        if not object_types:
            object_types = self._get_default_object_types()
        self._create_object_type_map(object_types)            
    
    def create(self, id, data):
        value_type = type(data[id])
        storage_object = self._object_type_map[value_type]
        return storage_object(id, data)

    def _create_object_type_map(self, object_types):
        for value_type, object_type in object_types:
            self._object_type_map[value_type] = object_type

    def _get_default_object_types(self):
        yield (list, CollectionObject)
        yield (dict, ComplexObject)
        yield (str, KeyValueObject)
        yield (int, KeyValueObject)
        yield (float, KeyValueObject)
        yield (bool, KeyValueObject)


class Storage(object):
    def __init__(self, data, object_factory):
        self.data = AttrDict(data)
        self._object_factory = object_factory
        self.create(self.data)

    def create(self, data):
        for object_name in data:
            storage_object = \
                self._object_factory.create(object_name, data)
            setattr(self, object_name, storage_object)

