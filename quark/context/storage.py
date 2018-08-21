import six, abc
from future.utils import viewitems
from future.builtins import super
from quark.repository import RepositoryFactory
from quark.exceptions import CollectionItemNotFoundException
from quark.common.events import EventHandler 


@six.add_metaclass(abc.ABCMeta)
class CollectionBase(object):
    def __init__(self, items):
        self.items = items
        self.collection_changed = EventHandler()

    def create(self, obj):
        self.items.append(obj.__dict__)
        self.collection_changed(self, action="create", element=obj)

    def get(self, obj):
        return self.get_item(obj)

    def delete(self, obj):
        self.items.remove(obj.__dict__)
        self.collection_changed(self, action="delete", element=obj)

    @abc.abstractclassmethod
    def update(self, obj):
        pass

    def get_item(self, obj):
        item = self.find(obj)
        if not item:
            raise CollectionItemNotFoundException("No matching item(s) found in the collection")
        return item

    def find(self, obj):
        for item in self.items:
            value_set = set(viewitems(item)).union(viewitems(obj))
            if len(value_set) <= len(item.keys()):
                return item


class RepositoryCollection(CollectionBase):
    def __init__(self, items):
        super().__init__(items)
    
    def get(self, obj):
        item = self.get_item(obj)    
        if item: return RepositoryFactory.create_from_args(item)

    def update(self, obj):
        item = self.get_item({"id":obj.id})
        
        if not item: return
        
        self.items.remove(item)
        self.items.append(obj.__dict__)
        self.collection_changed(self, action="update", element=obj)


class Storage(object):
    def __init__(self, name, config):
        self.name = name
        self._config = config
        self.storage_changed = EventHandler()

    def create_collection(self, collection_name, collection_type):
        if not issubclass(collection_type, CollectionBase):
            raise ValueError("Invalid collection type provided")
        collection = collection_type(self._config[collection_name])
        collection.collection_changed += self._on_collection_change
        setattr(self, collection_name, collection)

    def _on_collection_change(self, sender, **args):
        self.storage_changed(self)