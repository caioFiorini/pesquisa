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
import sys
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

#import matplotlib.pyplot as plt
#import networkx

# gr*.json contains the distance map in list of list style in JSON format
# Optimal solutions are : gr17 = 2085, gr24 = 1272, gr120 = 6942
with open("tsp/bays29_MATRIX.json", "r") as tsp_data:
    tsp = json.load(tsp_data)
distance_map = tsp["DistanceMatrix"]
IND_SIZE = tsp["TourSize"]
OPT_TOUR = tsp["OptTour"]
#----------------------------------------------------------------------------------
POPULACAO = 200
CROSSOVER=0.6
GERACOES=100
TAXA_MUTACAO = 0.001
TORNEIO=2
HALL_OF_FAME=5
#----------------------------------------------------------------------------------
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
    individual.value = distance
    return distance,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=TAXA_MUTACAO)
toolbox.register("select", tools.selTournament, tournsize=TORNEIO)
toolbox.register("evaluate", evalTSP)
#ELITISMO
#toolbox.register("select", selElitistAndTournament, frac_elitist=0.1 , tournsize=TORNEIO)

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
    random.seed(1)
    #random.seed(sys.argv[1])
    #print 'Seed: ',sys.argv[1]
	
    pop = toolbox.population(n=POPULACAO)
    offspring = toolbox.select(pop, len(pop))
	
    #pop[0] = creator.Individual([22, 26, 23, 7, 0, 27, 5, 11, 8, 4, 25, 28, 2, 1, 20, 19, 9, 3, 14, 17, 13, 21, 16, 10, 18, 15, 12, 24, 6])
    #print pop[0], evalTSP(pop[0])
	
    # Create the population and populate the history
    history = tools.History();
    toolbox.decorate("mate", history.decorator)
    #toolbox.decorate("mutate", history.decorator)


    # Inicializando cada individuo acrescentando uma lista vazia de pais
    for p in pop:
        p.pais = []

    hof = tools.HallOfFame(HALL_OF_FAME)
    stats1 = tools.Statistics(lambda ind: ind.fitness.values)
    stats1.register("1) Media   ", numpy.mean)
    # stats1.register("Mediana ", numpy.median)
    #stats1.register("Variancia   ", numpy.var)
    stats1.register("2) Desvio Padrao   ", numpy.std)
    stats1.register("3) Minimo  ", numpy.min)
    stats1.register("4) Maximo  ", numpy.max)
    # stats1.register("Histograma  ", numpy.histogram)
    # stats1.register("Count", numpy.ptp)

    stats2 = tools.Statistics(lambda ind: ind)
    stats2.register("Piores / Melhores  ", contaFilhos)
    stats2.register("Ind. Repetidos	 ", contaIndividuosIguais)
    
    stats = tools.MultiStatistics(Fitness=stats1, Filhos=stats2)

    # Parametros eaSimple: population, toolbox, cxpb (probability of mating two individuals),
    # mutpb (probability of mutating an individual), ngen (number of generation),
    # stats, halloffame (contais the best individuals), verbose (create or not the log statistics)

    algorithms.eaSimple(pop, toolbox, CROSSOVER, 1, GERACOES, stats=stats, halloffame=hof)

    #graph = networkx.DiGraph(history.genealogy_tree)
    #graph = graph.reverse()     # Make the grah top-down
    #colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    #networkx.draw(graph, node_color=colors)
    #plt.show()

    print('\nHALL OF FAME:')
    for elem in hof:
        print (elem, elem.fitness.values)

    import networkx
    from matplotlib.pyplot import show
    gen_best = history.getGenealogy(hof[0])
    graph = networkx.DiGraph(gen_best).reverse()
    networkx.draw(graph)
    show()

    b = datetime.datetime.now()
    c = b - a

    print '\n\nInicio : ', a.strftime("%A, %d %b %Y %H:%M:%S")
    print 'Termino: ', b.strftime("%A, %d %b %Y %H:%M:%S")
    print 'Duracao: ',divmod(c.days * 86400 + c.seconds, 60)
    return pop, stats, hof

if __name__ == "__main__":
    main()
