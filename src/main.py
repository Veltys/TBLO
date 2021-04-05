import lib
from tblo import Tblo


def main():
    tbloSphere = Tblo(500, 100, lib.sphere, fnLb = [-5, -5], fnUb = [5, 5])
    tbloAckley = Tblo(500, 100, lib.ackley, fnLb = [-20, -20], fnUb = [20, 20])
    tbloRastrigin = Tblo(500, 100, lib.rastrigin, fnLb = [-5, -5], fnUb = [5, 5])

    minX, minY = tbloSphere.optimize()

    evalResult = lib.sphere([minX, minY])

    print(f'Sphere MIN: x={minX}, y={minY}')
    print(f'Sphere({minX}, {minY}) = {round(evalResult, 4)}')

    minX, minY = tbloRastrigin.optimize()
    evalResult = lib.rastrigin([minX, minY])

    print(f'Rastrigin MIN: x={minX}, y={minY}')
    print(f'Rastrigin({minX}, {minY}) = {round(evalResult, 4)}')

    minX, minY = tbloAckley.optimize()
    evalResult = lib.ackley([minX, minY])

    print(f'Ackley MIN: x={minX}, y={minY}')
    print(f'Ackley({minX}, {minY}) = {round(evalResult, 4)}')

if __name__ == '__main__':
    main()
