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
        self.constraint = 100
        self.dimensions = 10
        self.export = True
        self.evals = 500000
        self.function = 'benchmark2020'
        self.iterations = 150000
        self.population = 50
        self.progress = True
        self.runs = 30
        self.verbosity = True
