#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import linecache
import os
import re
import sys

import numpy

import main as m


def parseClArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-fMin', type = int, default = 1, dest = 'fMin', help = 'minimum function id for benchmark 2020, default: 1; options: from 1 to 10')
    parser.add_argument('-fMax', type = int, default = 10, dest = 'fMax', help = 'maximum function id for benchmark 2020, default: 10; options: from 1 to 10; note: it has to be greater or equal to fMin')
    parser.add_argument('-fStep', type = int, default = 1, dest = 'fStep', help = 'function id step for benchmark 2020, default: 1; options: from 1 to 10')
    parser.add_argument('-dMin', type = int, default = 10, dest = 'dMin', help = 'minimum dimension, default: 10; options: 10, 15 or 20')
    parser.add_argument('-dMax', type = int, default = 20, dest = 'dMax', help = 'maximum dimension, default: 20; options: 10, 15 or 20; note: it has to be greater or equal to dMin')
    parser.add_argument('-dStep', type = int, default = 5, dest = 'dStep', help = 'dimension step, default: 5; options: from 1 to 20')
    parser.add_argument('-e', '-execute', type = bool, default = True, dest = 'execute', help = 'make execution phase; default True')
    parser.add_argument('-p', '-postprocessing', type = bool, default = True, dest = 'postprocessing', help = 'make postprocessing phase; default True')

    args = parser.parse_args(argv)

    return args


def guardar(alg, funcion, dimensiones, res):
    try:
        out = open(alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt', 'w')

    except IOError:
        print('Error de apertura del archivo <' + alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt>')
        print('ERROR: imposible abrir el archivo <' + alg + '_' + str(funcion) + '_' + str(dimensiones) + '.txt>', file = sys.stderr)

        exit(os.EX_OSFILE) # @UndefinedVariable

    else:
        for i in range(16):
            for j in range(30):
                out.write(str(res[i][j]))

                if j != 29:
                    out.write(',')

            # out.write(os.linesep)
            out.write("\n")

        out.close()


def posprocesar(dimensiones):
    # Recogida de todos los archivos de salida
    archivo = [ name for name in os.listdir('.') if os.path.isfile(os.path.join('.', name)) and re.match(r"^experiment-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.csv$", name) ]

    archivo = archivo[0]

    # Preparación de la matriz de resultados
    res = numpy.zeros((16, 30))

    for i in range(30):
        linea = linecache.getline(archivo, i * 2 + 3)

        linea = linea.split(',')

        for j in range(16):
            # Número de columna a leer
            numColumna = int(round((dimensiones ** (j / 5 - 3)) * 150000, 0))

            try: # Algunas líneas podrían no existir, debido a los criterios de parada
                elemento = linea[numColumna + 2]

            except IndexError: # En tal caso, se copia el resultado de la línea anterior
                res[j][i] = res[j - 1][i]

            else:
                res[j][i] = elemento

    os.remove(archivo)

    return res


def main(argv):
    # Preprocesamiento: variables

    alg = 'TBLO'

    args = parseClArgs(argv)

    for i in range(args.fMin - args.fStep, args.fMax, args.fStep):
        for j in range(args.dMin - args.dStep, args.dMax, args.dStep):
            if(args.execute):
                # Procesamiento: ejecución del programa
                print('Función ' + str(i + args.fStep) + ' dimensión ' + str(j + args.dStep))

                m.main(['-b', str(i + args.fStep), '-d', str(j + args.dStep)])

            if(args.postprocessing):
                # Posprocesamiento: recopilación de resultados
                guardar(alg, i + args.fStep, j + args.dStep, posprocesar(j + args.dStep))

if __name__ == '__main__':
    main(sys.argv[1:])

