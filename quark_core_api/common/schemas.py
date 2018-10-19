

APPLICATION_SCHEMA = {
    "workspaces" : {
        "$required" : ["id", "name", "dir"],
        "$unique"   : ["id", "name", "dir"],
        "$fields"   : {
            "id"   : {"$type" : int},
            "name" : {"$type" : str},
            "dir"  : {"$type" : str}
        }
    }
}