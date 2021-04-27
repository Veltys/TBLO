from operator import attrgetter
# import pprint as pp

import numpy as np
import random as rand


class Learner(object):
    def __init__(self, initialSubjects, initialFitness):
        super(Learner, self).__init__()

        self.subjects = initialSubjects
        self.fitness = initialFitness

    def __repr__(self):
        return f'<Learner s: {self.subjects} | f: {self.fitness} >'


class Tblo(object):
    learners = []


    def __init__(self, nPopulation, nGenerations, fnEval, *, fnLb, fnUb):
        super(Tblo, self).__init__()

        self.nPopulation = nPopulation
        self.nGenerations = nGenerations
        self.fnEval = fnEval
        self.fnLb = np.array(fnLb)
        self.fnUb = np.array(fnUb)


    def optimize(self):
        self.initialize()
        # pp.pprint(self.learners)

        for i, learner in enumerate(self.learners):
            learner.subjects, learner.fitness = self.teacherPhase(learner)
            learner.subjects, learner.fitness = self.learnerPhase(learner, i)

        # pp.pprint(self.learners)
        teacher = self.getTeacher()

        return teacher.subjects


    def initialize(self):
        self.learners = [self.createLearner() for _ in range(self.nPopulation)]


    def teacherPhase(self, learner):
        teacher = self.getTeacher()
        tf = rand.randint(1, 2)
        c = np.zeros(len(teacher.subjects))

        for i, subject in enumerate(learner.subjects):
            sMean = np.mean([s.subjects[i] for s in self.learners])
            r = rand.random()
            diffMean = teacher.subjects[i] - (tf * sMean)
            c[i] = subject + (r * diffMean)

        roundedC = np.around(c, decimals = 4)

        best, bestFitness = self.selectBest(learner.subjects, roundedC)

        return (best, bestFitness)


    def learnerPhase(self, learner, learnerIndex):
        kIndex = self.randomLearnerExcluding([learnerIndex])
        kLearner = self.learners[kIndex]
        kSubjets = kLearner.subjects
        c = np.zeros(len(learner.subjects))

        for i, subject in enumerate(learner.subjects):
            if learner.fitness < kLearner.fitness:
                diff = subject - kSubjets[i]
            else:
                diff = kSubjets[i] - subject

            r = rand.random()
            c[i] = subject + (r * diff)

        roundedC = np.around(c, decimals = 4)
        best, bestFitness = self.selectBest(learner.subjects, roundedC)

        return (best, bestFitness)


    def getTeacher(self):
        best = min(self.learners, key = attrgetter('fitness'))

        return best


    def selectBest(self, subjects, cSubjects):
        sFitness = self.fitness(subjects)
        cFitness = self.fitness(cSubjects)

        if sFitness > cFitness:
            best = cSubjects
            bestFitness = cFitness
        else:
            best = subjects
            bestFitness = sFitness

        return (best, bestFitness)


    def randomLearnerExcluding(self, excludedIndex):
        availableIndexes = set(range(self.nPopulation))
        excludeSet = set(excludedIndex)
        diff = availableIndexes - excludeSet
        selected = rand.choice(list(diff))

        return selected


    def fitness(self, solution):
        result = self.fnEval(solution)

        '''
        if result >= 0:
            fitness = 1 / (1 + result)
        else:
            fitness = abs(result)
        '''

        return np.around(result, decimals = 4)


    def createLearner(self):
        solution = Tblo.randomVector(self.fnLb, self.fnUb)
        fitness = self.fitness(solution)

        return Learner(solution, fitness)


    @staticmethod
    def randomVector(lb, ub):
        r = rand.random()
        solution = lb + (ub - lb) * r

        return np.around(solution, decimals = 4)
