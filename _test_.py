from quark_core_api.core import QuarkApplication
from quark_core_api.context import ApplicationContext
from quark_core_api.common import ContextInitializer
import json
import os

app_dir = os.path.expanduser("~\\")

app = QuarkApplication(ApplicationContext(app_dir, ContextInitializer.application))

location = "D:\\quark"

def create_ws(name, loc):
    return app.create_workspace(name, loc)


def create_xp(ws, name):
    return ws.create_experiment(name)

def create_script(ws, name):
    return ws.create_script(name,"{} script text goes here...".format(name))

def add_script(xp, stage, name):
    xp.add_script(stage, name)

def add_param(xp, name, value):
    xp.add_parameter(name, value)


def print_workspaces():
    for ws in app.workspaces:
        print(ws, app.workspaces[ws].name)


# create_xp(app.workspaces[20181001131931], "LGBM_CV")
# add_script(app.workspaces[20181001131931].experiments["LGBM_CV"], "prep", "preprocess")
# add_script(app.workspaces[20181001131931].experiments["LGBM_CV"], "prep", "remove_nan")
# add_script(app.workspaces[20181001131931].experiments["LGBM_CV"], "prep", "clean")

pipeline = app.workspaces[20181001131931].experiments["LGBM_CV"].pipeline

for s in pipeline.steps:
    print(s.name)

for s in pipeline.stages:
    print(s)






# from quark_core_api.context import ApplicationContext, ContextInitializer

# app_ctx_init = {
#     "workspaces": [{"id":1, "name":"ws-1", "dir":"home"}]
# }


# def test_application_context():
#     ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
#     ctx.create_storage("app")
#     print (ctx.workspaces[0])


# test_application_context()


