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

# import os
# path = os.path.expanduser(r"~\.quarkconfig2")

# p = Persistence()
# p.create_storage(filename=path, default_type="json", initializer=data)

# for i in p._quarkconfig_.repositories:
#     print(i)

# print(p._quarkconfig.user.name)
# print(p._quarkconfig.user.email)

# print(p._quarkconfig.tags[1])
# for s in p._quarkconfig.scores:
#     print(s)


# c = ApplicationContext()

# ws = c.create_workspace(20180921162635,"HomeCredit", "D:\\quark")
# print(ws)


app = Application()

app.create_workspace("HomeCredit", "D:\\quark")

print(app.workspaces)

# print(c.workspaces)

# ws.create_script("preprocess","preprocessing script text goes here...")
# exp = ws.create_experiment("LGBM")

# print(ws.experiments)



# print(c.create_workspace(5, "5", "c:/4"))
# print(c.create_workspace(5, "5", "c:/4"))

# print(c.workspaces)

# ws = WorkspaceContext("HomeCredit", "D:\\quark")
# # ws.create_script("data_loader2", "gsfdghdfgdfg")

# # print(ws.scripts)

# # exp = ws.create_experiment("lgbm")
# exp = ws.open_experiment("lgbm")
# print(exp.params)
