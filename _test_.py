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

