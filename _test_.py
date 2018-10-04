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



from quark_core_api.context import Application
import json

app = Application()

location = "D:\\quark"

def create_ws(name, loc):
    return app.create_workspace(name, loc)


def create_xp(ws, name):
    return ws.create_experiment(name)

def create_script(ws, name):
    return ws.create_script(name,"{} script text goes here...".format(name))

def add_script(xp, name):
    xp.add_script(name)

def add_param(xp, name, value):
    xp.add_parameter(name, value)


def print_workspaces():
    for ws in app.workspaces:
        print(ws, app.workspaces[ws].name)


# create_xp(app.workspaces[20181001131931], "LGBM_CV")
# add_script(app.workspaces[20181001131931].experiments["LGBM_CV"], "preprocess")
# add_script(app.workspaces[20181001131931].experiments["LGBM_CV"], "clean")

steps = app.workspaces[20181001131931].experiments["LGBM_CV"].pipeline.steps

for s in steps:
    print(s.name)