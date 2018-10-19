import sys

''' mock has been included in the built-in unittest library since Python 3.3
    This block intends to support Python 2.7 builds in which mock resides
    as a standalone package.'''
if sys.version_info.major == 3:
    from unittest import mock
    mock = mock
    builtins = "builtins"
else:
    import mock
    mock = mock
    builtins = "__builtin__"