#    This file is part of DEAP.
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
import json
from time import gmtime, strftime
import datetime
import pickle
import numpy
import sys
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

#import matplotlib.pyplot as plt
#import networkx

# gr*.json contains the distance map in list of list style in JSON format
# Optimal solutions are : gr17 = 2085, gr24 = 1272, gr120 = 6942

# parameters variation
#popSIZE = int(sys.argv[2])
#generationsNUMBER = int(sys.argv[3])
#crossXFACTOR = float(sys.argv[4])
#tournamentSIZE = int(sys.argv[5])
#mutationSIZE = float(sys.argv[6])
#elitismFACTOR = float(sys.argv[7])
#elitism_No_Individuals = int(sys.argv[8])

POPULACAO = int(sys.argv[2])
CROSSOVER=float(sys.argv[4])
GERACOES=int(sys.argv[3])
TAXA_MUTACAO = float(sys.argv[6])
TORNEIO=int(sys.argv[5])
HALL_OF_FAME=10  
ELITISMO = int(sys.argv[7])

with open("tsp/bays29_MATRIX.json", "r") as tsp_data:
    tsp = json.load(tsp_data)

distance_map = tsp["DistanceMatrix"]
IND_SIZE = tsp["TourSize"]
OPT_TOUR = tsp["OptTour"]
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)
toolbox = base.Toolbox()
history = tools.History()
# Attribute generator
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
    return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

def evalTSP(individual):
    distance = distance_map[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2]
    individual.value = 1/distance
    return 1/distance,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=TAXA_MUTACAO)
toolbox.register("evaluate", evalTSP)
#ELITISMO
if ELITISMO == 1:
    toolbox.register("select", selElitistAndTournament, frac_elitist=0.1 , tournsize=TORNEIO)
elif ELITISMO == 0:
    toolbox.register("select", tools.selTournament, tournsize=TORNEIO)


def mate_decorator(func):
    def wraper(ind1, ind2, *args, **kargs):
        pais = []
        for p in (ind1, ind2):
            pais.append(p.value)
        filhos = func(ind1, ind2, *args, **kargs)
        ret = filhos
        for f in filhos:
            f.pais = pais
        return ret
    return wraper

def contaFilhos(pop):
    numPiores = 0
    numMelhores = 0
    for f in pop:
        tot = 0
        count = 0
        for p in f.pais:
            count += 1
            tot += p
            # print p
        if count > 0:
            media = tot / count
            # print tot, count, media, f.value
            if f.value < media:
                numMelhores += 1
            elif f.value > media:
                numPiores += 1
        f.pais = []
    return numPiores, numMelhores

def contaIndividuosIguais(pop):
    numRepetidos = 0
    unicos = set()
    for i in range(len(pop)):
        unicos.add(tuple(pop[i]))
    return len(pop) - len(unicos)

# Decorate the variation operators
toolbox.decorate("mate", mate_decorator)
#toolbox.decorate("mutate", history.decorator)

def main():
    a = datetime.datetime.now()
    
    random.seed(sys.argv[1])
    
    pop = toolbox.population(n=POPULACAO)
    offspring = toolbox.select(pop, len(pop))
    
    #solucao gulosa bays29
    pop[0] = creator.Individual([22, 26, 23, 7, 0, 27, 5, 11, 8, 4, 25, 28, 2, 1, 20, 19, 9, 3, 14, 17, 13, 21, 16, 10, 18, 15, 12, 24, 6])

    #solucao gulosa brazil58
    #pop[0] = creator.Individual([4, 26, 42, 11, 56, 22, 23, 57, 43, 17, 0, 29, 12, 39, 24, 8, 31, 19, 52, 49, 3, 21, 7, 54, 53, 1, 40, 34, 9, 51, 50, 46, 48, 2, 47, 38, 28, 35, 16, 25, 5, 18, 27, 13, 36, 33, 45, 55, 44, 32, 14, 20, 10, 15, 37, 41, 30, 6])
    
    #solucao gulosa gr96
    #pop[0] = creator.Individual([89, 88, 87, 77, 84, 85, 83, 86, 90, 82, 80, 81, 69, 68, 56, 55, 57, 53, 52, 51, 49, 48, 42, 41, 40, 39, 38, 37, 36, 35, 31, 30, 29, 28, 0, 34, 33, 32, 43, 44, 45, 46, 47, 24, 23, 22, 21, 25, 27, 26, 64, 65, 66, 67, 63, 62, 61, 60, 59, 58, 70, 71, 72, 74, 73, 76, 75, 91, 92, 93, 95, 94, 20, 18, 19, 17, 16, 15, 14, 13, 12, 11, 9, 8, 6, 5, 4, 3, 7, 2, 1, 10, 50, 54, 78, 79])

    #solucao gulosa bier127
    #pop[0] = creator.Individual([116, 83, 80, 125, 81, 82, 74, 75, 77, 79, 78, 76, 17, 20, 16, 21, 3, 22, 23, 5, 105, 14, 107, 19, 18, 71, 7, 8, 10, 113, 104, 6, 0, 15, 1, 50, 56, 53, 44, 102, 43, 34, 35, 36, 40, 13, 11, 30, 26, 29, 42, 33, 38, 37, 25, 24, 32, 121, 27, 28, 31, 41, 39, 120, 4, 55, 123, 51, 49, 12, 114, 9, 119, 2, 89, 115, 59, 61, 60, 90, 57, 63, 99, 112, 65, 54, 46, 48, 52, 117, 47, 45, 93, 111, 110, 106, 126, 92, 94, 122, 96, 97, 100, 101, 62, 118, 95, 108, 86, 85, 84, 87, 109, 70, 69, 68, 67, 72, 73, 66, 58, 124, 88, 91, 98, 64, 103])

    #print pop[0], evalTSP(pop[0])
    
    # Create the population and populate the history
    history.update(pop)

    # Inicializando cada individuo acrescentando uma lista vazia de pais
    for p in pop:
        p.pais = []

    hof = tools.HallOfFame(HALL_OF_FAME)
    stats1 = tools.Statistics(lambda ind: ind.fitness.values)
    stats1.register("Media", numpy.mean)
    # stats1.register("Mediana ", numpy.median)
    #stats1.register("Variancia   ", numpy.var)
    stats1.register("Desvio_Padrao", numpy.std)
    stats1.register("Minimo", numpy.min)
    stats1.register("Maximo", numpy.max)
    # stats1.register("Histograma  ", numpy.histogram)
    # stats1.register("Count", numpy.ptp)

    stats0 = tools.Statistics(lambda ind: ind)
    stats0.register("Piores_Melhores", contaFilhos)
    stats0.register("Ind_Repetidos", contaIndividuosIguais)
    stats = tools.MultiStatistics(Filhos=stats0, Fitness=stats1)

    # Parametros eaSimple: population, toolbox, cxpb (probability of mating two individuals),
    # mutpb (probability of mutating an individual), ngen (number of generation),
    # stats, halloffame (contais the best individuals), verbose (create or not the log statistics)

    algorithms.eaSimple(pop, toolbox, CROSSOVER, 1, GERACOES, stats=stats, halloffame=hof)

    #graph = networkx.DiGraph(history.genealogy_tree)
    #graph = graph.reverse()     # Make the grah top-down
    #colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    #networkx.draw(graph, node_color=colors)
    #plt.show()

#    print('\nHALL OF FAME:')
#    for elem in hof:
#        print (elem, elem.fitness.values)

    b = datetime.datetime.now()
    c = b - a

#    print '\n\nInicio : ', a.strftime("%A, %d %b %Y %H:%M:%S")
#    print 'Termino: ', b.strftime("%A, %d %b %Y %H:%M:%S")
#    print 'Duracao: ',divmod(c.days * 86400 + c.seconds, 60)
    return pop, hof

if __name__ == "__main__":
    main()
