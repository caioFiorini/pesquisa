import random
import array
import datetime
import numpy
import sys
import csv
import os
import numpy
import copy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
#from deap import dtm

from Classificador import Classificador
from IOArquivo import LeituraArquivo

NUMERO_AMOSTRAS = 490
TAMANHO_TRANSFORMADA = 10

LISTACLASSES = ["Hidrolases", "Isomerases", "Liases", "Ligases", "Oxidoredutases", "Transferases"]
PATH_BASE = "BaseSting"
PATH_BASE_EXTERNA = "BaseExterna"
NOME_ARQUIVO_EXTERNO = 'BaseExterna_Reduzida.csv'
PATH_CLASSIFICADOR = "Individuos/"
#nomeArquivo = sys.argv[1]
nomeArquivo = 'TESTE'
NOMEARQUIVO_CLASSIFICADOR = nomeArquivo + ".csv"
MATRIZ_PROTEINAS = []
MATRIZ_PROTEINAS_EXTERNAS = []

def evaluate(individual):
    listaCaracteristicas = RetornaCaracteristica(individual)
    listaCaracteristicasExternas = RetornaCaracteristicaExternas(individual)
    MontaArquivoSVM(listaCaracteristicas, listaCaracteristicasExternas)
    fitness = ClassificadorCaracteristica(listaCaracteristicas)
    #fitness = 1 - fitness
    tamanho = listaCaracteristicas.__len__() + listaCaracteristicasExternas.__len__()
    return fitness, tamanho,

def RetornaCaracteristica(ind1):
    caracteristicas = []
    x = 0
    for i in ind1:
        if(x >= 50):
            return caracteristicas
        if(i == 1):
            caracteristicas.append(x)
        x = x + 1
    return caracteristicas

def RetornaCaracteristicaExternas(ind1):
    caracteristicas = []
    x = 0
    for i in ind1:
        if(x >= 51 and i == 1):
            valor = x - 51
            caracteristicas.append(valor)
        x = x + 1
    return caracteristicas

def MontaArquivoSVM(listaCaracteristicas, listaCaracteristicasExternas):
    ARQUIVO = open("Individuos/" + NOMEARQUIVO_CLASSIFICADOR, "w")
    leitor = LeituraArquivo(NUMERO_AMOSTRAS, LISTACLASSES, TAMANHO_TRANSFORMADA);
    leitor.BuildCSV(PATH_BASE, ARQUIVO, listaCaracteristicas, listaCaracteristicasExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS)
    ARQUIVO.close()
    return

def openTxt(path_Base, classe):
    caminho = os.path.join(path_Base, classe, classe + ".txt")
    arq = open(caminho, 'r')
    return arq

def CarregaProteinas(path_Base):
    contador = 0
    for numeroclasse, classe in enumerate(LISTACLASSES):
        listaProteinas = openTxt(path_Base, classe)

        for proteina in listaProteinas:
            with open(os.path.join(path_Base, classe, proteina.rstrip('\n').rstrip('\r')), 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                x = list(reader)
                MATRIZ_PROTEINAS.insert(contador, x)
                contador = contador + 1

def CarregaProteinasExternas(path_Base):
    with open(os.path.join(path_Base, NOME_ARQUIVO_EXTERNO.rstrip('\n').rstrip('\r')), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        x = list(reader)
        MATRIZ_PROTEINAS_EXTERNAS.insert(0, x)

def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
    return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

def ClassificadorCaracteristica(listaCaracteristicas):
    if(listaCaracteristicas.__len__() == 0):
        return 0
    svm = Classificador(PATH_CLASSIFICADOR, NOMEARQUIVO_CLASSIFICADOR)
    resultPrecision = svm.fitness()
    resultFMeasure = svm.fitness1()
    return resultFMeasure

def Melhor(pop):
    melhor = []
    fitness = 0
    for p in pop:
        if(fitness < p.fitness.values):
            melhor = p;
            fitness = p.fitness.values
    melhor = RetornaCaracteristica(melhor)
    return melhor

def mate_decorator(func):
    def wraper(ind1, ind2, *args, **kargs):
        pais = []
        for p in (ind1, ind2):
            pais.append(p.fitness.values)
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
        tot0 = 0
        tot1 = 0
        count = 0
        for p in f.pais:
            count += 1
            tot0 += p[0]
            tot1 += p[1]
            # print p
        if count > 0:
            media0 = tot0 / count
            media1 = tot1 / count
            # print tot, count, media, f.value
            if f.fitness.values[0] > media0 and f.fitness.values[1] <= media1:
                numMelhores += 1
            else:
                numPiores += 1
        f.pais = []
    return numPiores, numMelhores

def contaIndividuosIguais(pop):
    numRepetidos = 0
    unicos = set()
    for i in range(len(pop)):
        unicos.add(tuple(pop[i]))
    return len(pop) - len(unicos)

def InicializaPopulacao(pop):
    for p in pop:
        seed = random.randrange(1, 290)
        #print 'SEMENTE:', seed
        contador = 0
        for i in range(0, IND_SIZE):

            valor = random.randint(0, 1)
            if (seed == contador):
                break

            if (valor == 1):
                p[i] = valor
                contador = contador + 1

def RemoveReponhe(pop, tamanhoOriginal):
    for p in pop:
        if (p.fitness.values[1] == 0):
            pop.remove(p)

    while (tamanhoOriginal != len(pop)):
        seed = random.randrange(0, len(pop) - 1)
        copia = pop[seed]
        pop.insert(len(pop), copia)
    return pop

def ImprimeSaida(ngen, populacao, record):
    saida = ngen.__str__() + '\t' + len(populacao).__str__() + \
            '\t' + record['Filhos']['Ind. Repetidos\t '].__str__() + '\t' + record['Filhos']['Piores / Melhores  '].__str__() + \
            '\t' + record['Fitness']['2) Desvio Padrao   '][0].__str__() + '\t' +  record['Fitness']['2) Desvio Padrao   '][1].__str__() + \
            '\t' + record['Fitness']['4) Maximo  '][0].__str__() + '\t' + record['Fitness']['4) Maximo  '][1].__str__() + \
            '\t' + record['Fitness']['1) Media   '][0].__str__() + '\t' + record['Fitness']['1) Media   '][1].__str__() + \
            '\t' + record['Fitness']['3) Minimo  '][0].__str__() + '\t' +  record['Fitness']['3) Minimo  '][1].__str__()
            
    print (saida)

def eaMulti(population, toolbox, cxpb, mutpb, ngen, TAMANHO_POPULACAO, stats=None, halloffame=None, verbose=__debug__):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    population = RemoveReponhe(population, TAMANHO_POPULACAO)

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    ImprimeSaida(0, population, record)
    #if verbose:
    #    print logbook.stream

    # Avalia a populacao para ser utilizado no crownDistance
    population = toolbox.select(population, TAMANHO_POPULACAO)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        # offspring = toolbox.select(population, len(population))
        offspring = tools.selTournamentDCD(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        LOG_GERACOES = open("log/Geracao_" + nomeArquivo + '.txt', "a+")
        LOG_GERACOES.write('Classificando geracao: ' + gen.__str__() + ' Hora: ' + datetime.datetime.now().__str__() + '\n')

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        offspring = RemoveReponhe(offspring, TAMANHO_POPULACAO)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Select the next generation population
        population = toolbox.select(population + offspring, TAMANHO_POPULACAO)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        ImprimeSaida(gen, population, record)
        #if verbose:
        #    print logbook.stream

    return population, logbook

def varAnd(population, toolbox, cxpb, mutpb):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their
              parents.

    The variation goes as follow. First, the parental population
    :math:`P_\mathrm{p}` is duplicated using the :meth:`toolbox.clone` method
    and the result is put into the offspring population :math:`P_\mathrm{o}`.
    A first loop over :math:`P_\mathrm{o}` is executed to mate pairs of consecutive
    individuals. According to the crossover probability *cxpb*, the
    individuals :math:`\mathbf{x}_i` and :math:`\mathbf{x}_{i+1}` are mated
    using the :meth:`toolbox.mate` method. The resulting children
    :math:`\mathbf{y}_i` and :math:`\mathbf{y}_{i+1}` replace their respective
    parents in :math:`P_\mathrm{o}`. A second loop over the resulting
    :math:`P_\mathrm{o}` is executed to mutate every individual with a
    probability *mutpb*. When an individual is mutated it replaces its not
    mutated version in :math:`P_\mathrm{o}`. The resulting
    :math:`P_\mathrm{o}` is returned.

    This variation is named *And* beceause of its propention to apply both
    crossover and mutation on the individuals. Note that both operators are
    not applied systematicaly, the resulting individuals can be generated from
    crossover only, mutation only, crossover and mutation, and reproduction
    according to the given probabilities. Both probabilities should be in
    :math:`[0, 1]`.
    """
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

#Individuo and #Operator genetic
IND_SIZE = 104
#POPULACAO = int(sys.argv[2])
#CROSSOVER=float(sys.argv[4])
#GERACOES=int(sys.argv[3])
#TAXA_MUTACAO = float(sys.argv[6])
#TORNEIO=int(sys.argv[5])
#HALL_OF_FAME = 10
#ELITISMO = int(sys.argv[7])

POPULACAO = 1
TORNEIO = 2
CROSSOVER = 0.9
TAXA_MUTACAO = 0.001
GERACOES = 2
HALL_OF_FAME = 10
ELITISMO = 1

# Function Max
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMulti)

# Attribute generator
toolbox = base.Toolbox()
toolbox.register("indices", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operadores genetic
toolbox.register("select", tools.selNSGA2)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=TAXA_MUTACAO)
toolbox.register("evaluate", evaluate)
toolbox.decorate("mate", mate_decorator)
hof = tools.HallOfFame(HALL_OF_FAME)
#toolbox.register("map", dtm.map)

def main():
    a = datetime.datetime.now()
    #random.seed(sys.argv[1])
    random.seed(1)

    CarregaProteinas(PATH_BASE)
    CarregaProteinasExternas(PATH_BASE_EXTERNA)

    pop = toolbox.population(n=POPULACAO)
    for p in pop:
        p.pais = []

    for p in pop:
        for i in range(0, IND_SIZE):
            if(i == 0 or i == 1 or i == 50 or
               i == 51 or i == 52 or i == 103):
                p[i] = 1
            else:
                p[i] = 0

    stats1 = tools.Statistics(lambda ind: ind.fitness.values)
    stats1.register("1) Media   ", numpy.mean,axis=0)
    stats1.register("2) Desvio Padrao   ", numpy.std,axis=0)
    stats1.register("3) Minimo  ", numpy.min,axis=0)
    stats1.register("4) Maximo  ", numpy.max,axis=0)

    stats2 = tools.Statistics(lambda ind: ind)
    stats2.register("Piores / Melhores  ", contaFilhos)
    stats2.register("Ind. Repetidos	 ", contaIndividuosIguais)

    stats = tools.MultiStatistics(Fitness=stats1, Filhos=stats2)

    eaMulti(pop, toolbox, CROSSOVER, 1, GERACOES, POPULACAO, stats=stats, halloffame=hof)
    
    MELHORES = open("melhores/" + nomeArquivo + '.txt', "a+")
    MELHORES.write('\nHALL OF FAME:')
    for elem in hof:
        MELHORES.write(elem.__str__() + elem.fitness.values.__str__() + '\n')

    #print('\nHALL OF FAME:')
    #for elem in hof:
    #    print (elem, elem.fitness.values)

    #b = datetime.datetime.now()
    #c = b - a

    #print '\n\nInicio : ', a.strftime("%A, %d %b %Y %H:%M:%S")
    #print 'Termino: ', b.strftime("%A, %d %b %Y %H:%M:%S")
    #print 'Duracao: ', divmod(c.days * 86400 + c.seconds, 60)

if __name__ == "__main__":
    main()




