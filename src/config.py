# -*- coding: utf-8 -*-


'''!
    @file:           config.py
    @brief:          Configuration module

    @author:         Rafael Carlos Méndez Rodríguez (i82meror)
    @date:           2021-04-23
    @version:        1.3.0
    @usage:          import Config | from Config import ...
    @note:           Not intended for direct execution
'''


class ConfigSingleton(type):
    '''! Metaclase con las herramientas para hacer que una clase hija se comporte con el patrón de código Singleton'''

    _instances = {}

    def __call__(self, *args, **kwargs):
        '''! Método "mágico" que es llamado cuando se invoca una clase
    
            @param *args:       Argumentos posicionales de la clase
            @param **kwargs:    Argumentos con nombre de la clase

            @return:            Instancia de la clase
        '''

        if self not in self._instances:
            self._instances[self] = super(ConfigSingleton, self).__call__(*args, **kwargs)

        return self._instances[self]


class Config(metaclass = ConfigSingleton):
    '''! Clase que almacena la configuración predeterminada del sistema
        Hace uso de patrón Singleton para tener persistencia a lo largo de todo el código
    '''

    def __init__(self):
        '''! Inicializador de la clase'''

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
