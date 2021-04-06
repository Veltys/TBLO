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
