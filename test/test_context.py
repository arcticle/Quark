import pytest
from test.testsetup import mock, builtins
from quark_core_api.context import ApplicationContext, WorkspaceContext, ExperimentContext
from quark_core_api.common import ContextInitializer

app_ctx_init = {
    "workspaces": [{"id":1, "name":"ws-1", "dir":"home"}]
}

ws_ctx_init = {
    "experiments": ["xpr-1"],
    "scripts": ["scr-1"]
}

xp_ctx_init = {
    "pipeline": {"preprocess":["prep_data"], "clean":["clean_data"]},
    "params": {"learning_rate":0.1}
}

def test_application_context_workspace_exist():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.workspaces[0]["id"] == 1

def test_application_context_create_workspace_check_created_id():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.create_workspace(2, "ws-1", "home") == 2

def test_application_context_create_workspaces_check_count():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    ctx.create_workspace(2, "ws-1", "home")
    ctx.create_workspace(3, "ws-1", "home")
    assert len(ctx.workspaces) == 3

def test_application_context_get_workspace_no_storage_exception():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    with pytest.raises(Exception):
        assert ctx.workspaces

def test_application_context_create_workspace_no_storage_exception():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    with pytest.raises(Exception):
        ctx.create_workspace(2, "ws-1", "home")

def test_application_context_query_workspace_by_id():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.get_workspace(id=1)["id"] == 1 

def test_application_context_query_workspace_by_name():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.get_workspace(name="ws-1")["name"] == "ws-1" 

def test_application_context_query_workspace_by_directory():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.get_workspace(directory="home")["dir"] == "home"

def test_application_context_query_workspace_by_directory_from_many():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    ctx.create_workspace(2, "ws-2", "home2")
    ctx.create_workspace(3, "ws-3", "home3")
    assert ctx.get_workspace(directory="home2")["dir"] == "home2"

def test_application_context_delete_workspace_check_deleted_id():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.delete_workspace(1) == 1

def test_application_context_delete_workspace_check_count():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    ctx.delete_workspace(1)
    assert len(ctx.workspaces) == 0

def test_application_context_delete_workspace_invalid_id_returns_minus_one():
    ctx = ApplicationContext(None, ContextInitializer(app_ctx_init, None))
    ctx.create_storage("app_test")
    assert ctx.delete_workspace(2) == -1

def test_workspace_context_check_experiment():
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    assert ctx.experiments[0] == "xpr-1" and len(ctx.experiments) == 1

def test_workspace_context_check_script():
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    assert ctx.scripts[0] == "scr-1" and len(ctx.scripts) == 1

def test_workspace_context_create_experiment():
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    assert ctx.create_experiment("xpr-2") == 1 and len(ctx.experiments) == 2

def test_workspace_context_delete_experiment():
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    ctx.create_experiment("xpr-2")
    assert ctx.delete_experiment("xpr-2") == 1 
    assert len(ctx.experiments) == 1 
    assert ctx.experiments[0] == "xpr-1"

@mock.patch("quark_core_api.context.WorkspaceContext.create_file")
def test_workspace_context_create_script(create_file):
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    assert ctx.create_script("scr-2", "test script") == 1
    assert len(ctx.scripts) == 2
    assert create_file.called

@mock.patch("quark_core_api.context.WorkspaceContext.create_file")
def test_workspace_context_delete_script(create_file):
    ctx = WorkspaceContext(None, ContextInitializer(ws_ctx_init, None))
    ctx.create_storage("ws_test")
    ctx.create_script("scr-2", "test script")
    assert ctx.delete_script("scr-1")
    assert len(ctx.scripts) == 1
    assert ctx.scripts[0] == "scr-2"

def test_experiment_context_check_pipeline():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.pipeline["preprocess"]
    assert ctx.pipeline["clean"]
    assert len(ctx.pipeline) == 2

def test_experiment_context_check_params():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.params["learning_rate"] == 0.1

def test_experiment_context_add_script():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.add_script("preprocess","scr-1") == 1
    assert len(ctx.pipeline["preprocess"]) == 2
    assert len(ctx.pipeline["clean"]) == 1

def test_experiment_context_remove_script():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.remove_script("preprocess", "prep_data") == 1
    assert len(ctx.pipeline["preprocess"]) == 0
    assert len(ctx.pipeline["clean"]) == 1

def test_experiment_context_remove_stage():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.remove_stage("preprocess") == 1
    assert "preprocess" not in ctx.pipeline
    assert len(ctx.pipeline["clean"]) == 1

def test_experiment_context_add_param():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.add_parameter("num_iteration", 1000) == 1
    assert ctx.params["num_iteration"] == 1000

def test_experiment_context_remove_param():
    ctx = ExperimentContext(None, ContextInitializer(xp_ctx_init, None))
    ctx.create_storage("xp_test")
    assert ctx.remove_parameter("learning_rate") == 1
    assert "learning_rate" not in ctx.params