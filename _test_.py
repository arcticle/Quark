import copy
# from quark.storage import StorageObjectFactory, Storage



# data = {
#     "repositories": [
#         {"id":1, "name":"Repo-1", "dir":"c:/repos/repo1"},
#         {"id":2, "name":"Repo-2", "dir":"c:/repos/repo2"},
#         {"id":3, "name":"Repo-3", "dir":"c:/repos/repo3"}
#     ],

#     "user": {"name":"John Doe", "email":"john@doe.com"},

#     "repo_limit" : 10,

#     "tags" : [
#         "Data Analytics 101",
#         "Artificial Intelligence",
#         "Arcticle",
#         "Quark"
#     ],

#     "scores" : [100, 200, 300, 400]
# }






# storage = Storage(copy.deepcopy(data), StorageObjectFactory())
# print(storage.objects)



from quark.core.data.persistence import Persistence
from quark.core.context import ApplicationContext, WorkspaceContext
from quark.core.context import Application
import json

app = Application()

ws = app.create_workspace("HomeCredit", "D:\\quark")

xp = ws.create_experiment("LGBM")
ws.create_script("preprocess","preprocessing script text goes here...")

xp.add_script("preprocess")
xp.add_parameter("learning_rate", 0.1)

# from future.utils import viewitems
# from collections.abc import Mapping

# class Pipeline(Mapping):
#     def __init__(self, *args, **kw):
#         self._scripts = dict()
#         self._steps = []

#         if args:
#             for script in args:
#                 self.__addstep__(script.name, script)

#         if kw:
#             for name, script in viewitems(kw):
#                 self.__addstep__(name, script)

#     @property
#     def num_of_steps(self):
#         return len(self._scripts)

#     def add_step(self, script):
#         self.__addstep__(script.name, script)
        

#     def __getitem__(self, key):
#         if isinstance(key, int):
#             if key == -1:
#                 return self._scripts[self.num_of_steps-1]
#             return self._scripts[key]
#         if isinstance(key, str):
#             index = self._steps.index(key)
#             return self._scripts[index]

#     def __iter__(self):
#         for step in range(self.num_of_steps):
#             yield self._scripts[step]
    
#     def __len__(self):
#         return len(self._scripts)

#     def __addstep__(self, name, script):
#         key = len(self._scripts)
#         self._scripts[key] = script
#         self._steps.insert(key, name)

# class a(object):
#     def __init__(self, name):
#         self._name = name

#     @property
#     def name(self):
#         return self._name

# # pp = Pipeline(z=a("z"), x=a("x"), y=a("y"))
# pp = Pipeline(a("z"), a("x"), a("y"))
# pp.add_step(a("j"))

# print(pp._scripts)
# print(pp[0].name)
# print(pp["y"].name)
# print(pp[-1].name)

# for i in pp:
#     print (i.name)