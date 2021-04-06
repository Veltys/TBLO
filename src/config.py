# -*- coding: utf-8 -*-


class ConfigSingleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(ConfigSingleton, self).__call__(*args, **kwargs)

        return self._instances[self]


class Config(metaclass = ConfigSingleton):
    def __init__(self):
        self.benchmark = 1
        self.dimensions = 10
        self.evals = 500000
        self.verbosity = False
