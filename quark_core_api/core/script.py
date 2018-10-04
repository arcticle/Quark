import os, copy


class Script(object):
    def __init__(self, name, directory):
        self._name = name
        self._filename = os.path.join(directory, "{}.py".format(name))

    @property
    def name(self):
        return self._name

    @property
    def filename(self):
        return self._filename

    def run(self, context):
        pass
