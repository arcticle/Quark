from quark.storage import Storage, StorageObjectFactory, data


s = Storage(data, StorageObjectFactory())
print(s.repositories.find({"id":{"$gte":2}}))

