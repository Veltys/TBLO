#!/usr/bin/env python3


import csv
import getopt
from itertools import chain
import os
import sys
import time

import config
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

    optimizer = 'TBLO'

    # CSV file header
    header = []

    for i in range(cnf.iterations):
        header.append(f'It{i + 1}')

    try:
        if cnf.export:
            out = open(f'.{os.sep}{time.strftime("%Y-%m-%d-%H-%M-%S")}-experiment.csv', 'a')

    except IOError:
        print(f'Error de apertura del archivo <{time.strftime("%Y-%m-%d-%H-%M-%S")}-experiment.csv>')
        print(f'ERROR: imposible abrir el archivo <{time.strftime("%Y-%m-%d-%H-%M-%S")}-experiment.csv>', file = sys.stderr)

        exit(os.EX_OSFILE) # @UndefinedVariable

    else:
        if cnf.verbosity:
            print(f'{optimizer} is optimizing with {cnf.function.__name__}')

        if cnf.export == True:
            csvOut = csv.writer(out, delimiter = ',')

            csvOut.writerow(chain.from_iterable([['Optimizer' + 'objfname' + 'ExecutionTime'], header]))

        res = []

        for i in range(cnf.runs):
            if cnf.verbosity:
                print(f'Run {i + 1} of {cnf.runs}')

            timerStart = time.time()

            for _ in range(cnf.iterations):
                tbloBenchmark = Tblo(50, 100, cnf.function, fnLb = [-100, -100], fnUb = [100, 100])

                res.append(cnf.function(tbloBenchmark.optimize()))


            timerEnd = time.time()

            if cnf.export:
                csvOut.writerow(chain.from_iterable([[optimizer, cnf.function.__name__, timerEnd - timerStart], res]))


        if cnf.export:
            out.close()


if __name__ == '__main__':
    main(sys.argv[1:])
