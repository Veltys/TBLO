import ctypes
import os

import config
import numpy as np


def sphere(d):
    return np.sum([x ** 2 for x in d])


def sphereFn():
    def fn(*args):
        return sum([sphere(d) for _, d in enumerate(args)])
    return fn


def ackley(d, *, a = 20, b = 0.2, c = 2 * np.pi):
    sumPart1 = np.sum([x ** 2 for x in d])
    part1 = -1.0 * a * np.exp(-1.0 * b * np.sqrt((1.0 / len(d)) * sumPart1))

    sumPart2 = np.sum([np.cos(c * x) for x in d])
    part2 = -1.0 * np.exp((1.0 / len(d)) * sumPart2)

    return a + np.exp(1) + part1 + part2


def ackleyFn():
    def fn(*args):
        return sum([ackley(d) for _, d in enumerate(args)])
    return fn


def rastrigin(d):
    sumI = np.sum([x ** 2 - 10 * np.cos(2 * np.pi * x) for x in d])
    return 10 * len(d) + sumI


def rastriginFn():
    def fn(*args):
        return sum([rastrigin(d) for _, d in enumerate(args)])

    return fn


def benchmark2020(x):
    cnf = config.Config()

    libtest = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'libbenchmark.' + ('dll' if os.name == 'nt' else 'so'))
    libtest.cec20_bench.argtypes = ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_double * len(x)), ctypes.c_ushort
    libtest.cec20_bench.restype = ctypes.c_double

    return libtest.cec20_bench(1, len(x), (ctypes.c_double * len(x))(*x), cnf.benchmark)


def benchmark2020Fn():
    def fn(*args):
        return sum([benchmark2020(d) for _, d in enumerate(args)])

    return fn
