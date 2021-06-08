#!/usr/bin/env python3


'''!
    @file:           main.py
    @brief:          Main program

    @author:         Rafael Carlos Méndez Rodríguez (i82meror)
    @date:           2021-05-14
    @version:        1.6.2
    @usage:          python3 run_script.py
    @note:           Use flag -h to see optional commands and help
'''


import argparse
import csv
import errno
from itertools import chain
import os
import sys
import time

import progressbar

import config
import lib
from tblo import Tblo


def parseClArgs(argv):
    '''! Procesa los argumentos pasados al programa
    
        @param argv:    Vector de argumentos
    
        @return:        Argumentos procesados
    '''

    cnf = config.Config()

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type = int, default = cnf.benchmark, dest = 'benchmark', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'benchmark 2020 function id, default: 1; options: from 1 to 10')
    parser.add_argument('-c', type = float, default = cnf.constraint, dest = 'constraint', help = 'solution constraint value, default: 100')
    parser.add_argument('-d', type = int, default = cnf.dimensions, dest = 'dimensions', choices = [10, 15, 20], help = 'dimensions, default: 10')
    parser.add_argument('-e', type = bool, default = cnf.export, dest = 'export', help = 'enable for export data to CSV, default: True (export)')
    parser.add_argument('-f', type = str, default = cnf.function, dest = 'function', choices = ['sphere', 'ackley', 'rastrigin', 'benchmark2020'], help = 'function to be optimized, default: benchmark2020')
    parser.add_argument('-i', type = int, default = cnf.iterations, dest = 'iterations', help = 'number of iterations, default: 150000')
    parser.add_argument('-m', type = int, default = cnf.evals, dest = 'evals', help = 'maximum evaluations, default: 500.000')
    parser.add_argument('-p', type = int, default = cnf.population, dest = 'population', help = 'number of solutions per generation, default: 50')
    parser.add_argument('-r', type = int, default = cnf.runs, dest = 'runs', help = 'number of runs, default: 30')
    parser.add_argument('-s', type = bool, default = cnf.progress, dest = 'progress', help = 'shown progress bar, default: True')
    parser.add_argument('-v', type = bool, default = cnf.verbosity, dest = 'verbosity', help = 'enable for verbosity, default: False (no verbose)')

    args = parser.parse_args(argv)

    return args


def storeNewConfig(args):
    '''! Valida y almacena la nueva configuración
    
        @param args:    Argumentos a almacenar
    
        @return:        Si la configuración es válida y, por ende, se ha almacenado
    '''

    cnf = config.Config()

    funcs = {
        'sphere': lib.sphere,
        'ackley': lib.ackley,
        'rastrigin': lib.rastrigin,
        'benchmark2020': lib.benchmark2020,
    }

    if (args.function == 'benchmark2020' or args.function == lib.benchmark2020) and (args.benchmark < 1 or args.benchmark > 10):
        print(f'Invalid supplied benchmark id {args.benchmark}. Ensure benchmark id is valid or use command line options.')

        return False
    elif (isinstance(args.function, str) and args.function not in funcs) or (callable(args.function) and args.function not in funcs.values()):
        print(f'Missing supplied function {args.function} definition. Ensure function defintion exists or use command line options.')

        return False
    else:
        for name, arg in vars(args).items():
            setattr(cnf, name, arg)

        if (not callable(args.function)):
            cnf.function = funcs[cnf.function]

        return True


def tlbo(csvOut):
    '''! Ejecuta el algoritmo TBLO
    
        @param csvOut:  Archivo de salida
    '''

    optimizer = 'TBLO'

    cnf = config.Config()

    if cnf.verbosity:
        print(f'{optimizer} is optimizing with {cnf.function.__name__}')

    for _ in range(cnf.runs):
        if cnf.progress:
            pb = progressbar.ProgressBar(max_value = cnf.evals)

        res = []
        evals = 0

        if cnf.progress:
            pb.update(evals)

        timerStart = time.time()

        tbloBenchmark = Tblo(cnf.population, cnf.iterations, cnf.function, fnLb = -cnf.constraint, fnUb = cnf.constraint, dim = cnf.dimensions)

        for _ in range(cnf.iterations):
            tbloBenchmark.optimize()

            res.append(tbloBenchmark.getTeacher().fitness)

            evals += cnf.population

            if cnf.progress:
                pb.update(evals)

            if evals >= cnf.evals:
                if cnf.progress:
                    # pb.update(cnf.evals)
                    pb.finish()

                break

        if cnf.progress:
            pb.finish()

        timerEnd = time.time()

        if cnf.export:
            csvOut.writerow(chain.from_iterable([[optimizer, cnf.function.__name__, timerEnd - timerStart], res]))


def main(argv):
    '''! Ejecuta el algoritmo TBLO y exporta, de estar configurado así, los resultados a formato CSV
    
        @param argv:    Vector de argumentos
    
        @return:        Código de retorno
    '''

    NOMBRE_ARCHIVO = f'experiment-{time.strftime("%Y-%m-%d-%H-%M-%S")}.csv'

    args = parseClArgs(argv)

    cnf = config.Config()

    if not storeNewConfig(args):
        sys.exit(errno.EPERM)
    else:
        try:
            if cnf.export:
                out = open(f'.{os.sep}{NOMBRE_ARCHIVO}', 'a')

        except IOError:
            print(f'Error de apertura del archivo <{NOMBRE_ARCHIVO}>')
            print(f'ERROR: imposible abrir el archivo <{NOMBRE_ARCHIVO}>', file = sys.stderr)

            sys.exit(errno.ENOENT)

        else:
            if cnf.export:
                # CSV file header
                header = []

                for i in range(cnf.iterations):
                    header.append(f'It{i + 1}')

                csvOut = csv.writer(out, delimiter = ',')
                csvOut.writerow(chain.from_iterable([['Optimizer', 'objfname', 'ExecutionTime'], header]))

            tlbo(csvOut)

            if cnf.export:
                out.close()

            if cnf.progress:
                print()


if __name__ == '__main__':
    main(sys.argv[1:])
