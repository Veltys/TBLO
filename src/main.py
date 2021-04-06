#!/usr/bin/env python3


import getopt
import sys

import config
import lib
from tblo import Tblo


def main(argv):
    cnf = config.Config()

    try:
        opts, _ = getopt.getopt(
            argv,
            'b:d:v',
            [
                'bench=',
                'dim=',
            ]
        )

    except getopt.GetoptError:
        print('Usage: main.py [-b benchmark_id or --bench=benchmark_id] [-d dimensions or --dim=dimensions] [-v]')

        sys.exit(2)


    for opt, arg in opts:
        if opt in ('-b', '--bench'):
            cnf.benchmark = int(arg)

        elif opt in ('-d', '--dim'):
            cnf.dimensions = int(arg)

        elif opt in ('-v'):
            cnf.verbosity = True


    tbloBenchmark = Tblo(50, 150000, lib.benchmark2020, fnLb = [-100, -100], fnUb = [100, 100])

    minX, minY = tbloBenchmark.optimize()
    evalResult = lib.benchmark2020([minX, minY])

    print(f'Benchmark2020 MIN: x={minX}, y={minY}')
    print(f'Benchmark2020({minX}, {minY}) = {round(evalResult, 4)}')


if __name__ == '__main__':
    main(sys.argv[1:])
