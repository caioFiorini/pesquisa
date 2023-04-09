import random 
import array
import datetime
import numpy
import csv
import os

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from Classificador import Classificador
from IOArquivo import LeituraArquivo

NUMERO_AMOSTRAS = 151
TAMANHO_TRANSFORMADA = 2

LISTACLASSES = ["Iris-virginica", "Iris-setosa", "Iris-versicolor"]
PATH_BASE = "BaseIris"
#NOME_ARQUIVO_EXTERNO = "BaseExterna_reduzida.csv"
PAHT_CLASSIFICADOR = "Individuos/"

nomeArquivo = 'TESTE2'
NOME_ARQUIVO_CLASSIFICADOR = nomeArquivo + ".csv"
MATRIZ_FLORES = []
#MATRIZ_FLORES_EXTERNAS = []

def evaluate(individual):
    listaCaracteristicas = RetornaCaracteristica(individual)
    #listaCaracteristicasExternas = RetornaCaracteristicaExternas(individual)
    MontarArquivoSVM(listaCaracteristicas)
    fitness = ClassificadorCaracteristica(listaCaracteristicas)

    tamanho = listaCaracteristicas._len_()
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

# def RetornaCaracteristicaExternas(ind1):
#     caracteristicas = []
#     x = 0
#     for i in ind1: 
#         if(x >= 51 and i == 1):
#             valor = x - 51
#             caracteristicas.append(valor)
#         x = x + 1
#     return caracteristicas

def MontarArquivoSVM(listaCaracteristicas):
    ARQUIVO = open("Individuos/" + NOME_ARQUIVO_CLASSIFICADOR, "w")
    leitor = LeituraArquivo(NUMERO_AMOSTRAS, LISTACLASSES, TAMANHO_TRANSFORMADA)
    leitor.BuildCSV(PATH_BASE, ARQUIVO, listaCaracteristicas, MATRIZ_FLORES)
    ARQUIVO.close()
    return

def openTxt(path_Base, classe):
    caminho = os.path.join(path_Base, classe, classe + ".txt")
    arq = open(caminho, 'r')
    return arq

# def CarregaFlor(path_Base):
#     contador = 0
#     for numeroclasse, classe in enumerate(LISTACLASSES):
#         listaFlores = openTxt(path_Base, classe)

#         for flores in listaFlores: 
#             with open(os.path.join(path_Base, classe, flores.rstrip('\n').rstrip('\r')), 'r') as csvfile:
#                 reader = csv.reader(csvfile, delimiter=';')
#                 x = list(reader)
#                 MATRIZ_FLORES.insert(contador, x)
#                 contador = contador + 1

def CarregaFlor (path_Base):
    with open(os.path.join(path_Base, "iris.csv"), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        #print(reader)
        x = list(reader)
        MATRIZ_FLORES.insert(0, x)

def selElitistAndTournamente(individuals, k, frac_elitist, tournsize):
    return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

def ClassificadorCaracteristica(listaCaracteristicas):
    if(listaCaracteristicas.__len__() == 0):
        return 0
    svm = Classificador(PAHT_CLASSIFICADOR, NOME_ARQUIVO_CLASSIFICADOR)
    resultPrecision = svm.fitness()
    resultFMeasure = svm.fitness1()
    return resultFMeasure

def Melhor(pop):
    melhor = []
    fitness = 0
    for p in pop: 
        if(fitness < p.fitness.values):
            melhor = p
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
            
        if count > 0:
            media0 = tot0 / count
            media1 = tot1 / count

            if f.fitness.values[0] > media0 and f.fitness.values[1] <= media1:
                numPiores += 1
            else:
                numPiores += 1
        f.pais = []
    return numPiores, numMelhores

def contaIndividuosIguais(pop):
    numRepetidos = 0
    unicos =set()
    for i in range(len(pop)):
        unicos.add(tuple(pop[i]))
    return len(pop) - len(unicos)

def IncializaPopulação(pop):
    for p in pop:
        seed = random.randrange(1 , 290)
        contador = 0
        for i in range(0, IND_SIZE):
            valor = random.randint(0,1)
            if(seed == contador):
                break
            
            if(valor == 1):
                p[1] == valor
                contador = contador + 1

def RemoveReponhe(pop, tamanhoOriginal):
    for p in pop:
        if (p.fitness.values[1] == 0):
            pop.remove(p)
    
    while(tamanhoOriginal != len(pop)):
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

def eaMulti(population, toolbox, cxpb, mutpb, ngen, TAMANHO_POPULACAO, stats = None, halloffame = None, verbose = __debug__):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    #Evaluate the individuals with on invalid fitness
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
    
    #Avalia a população para ser utilizado no crownDistance
    population = toolbox.select(population,TAMANHO_POPULACAO)

    #Inpicio da geração populacional
    for gen in range(1, ngen + 1):
        #Seleciona a proxima geração de indivíduos
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        LOG_GERACOES = open("log/Geracao_" + nomeArquivo + '.txt', "ta+")
        LOG_GERACOES.write('Classificando geracao: ' +  gen.__str__() + 'Hora: ' + datetime.datetime.now().__str__() + '\n')

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip (invalid_ind, fitnesses):
            ind.fitness.values = fit

        offspring = RemoveReponhe(offspring, TAMANHO_POPULACAO)

        #Update the Hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        #Seleciona a próxima geração da população
        population = toolbox.select(population + offspring, TAMANHO_POPULACAO)

        record = stats.compile(population) if stats else {}
        logbook.record(gen= gen, nevals=len(invalid_ind), **record)
        ImprimeSaida(gen, population, record)

    return population, logbook

def varAnd(population, toolbox, cxpb, mutpb):
    offspring = [toolbox.clone(ind) for ind in population]

    #Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values
    
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

#Individuo and Operator genetic
IND_SIZE = 104
POPULACAO = 1
TORNEIO = 2
CROSSOVER = 0.9
TAXA_MUTACAO = 0.001
GERACOES = 2
HALL_OF_FAME = 10
ELITISMO = 1

#Function Max
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMulti)

#Atributo gerador
toolbox = base.Toolbox()
toolbox.register("indices", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#Operadores genéticos
toolbox.register("select", tools.selNSGA2)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=TAXA_MUTACAO)
toolbox.register("evaluate", evaluate)
toolbox.decorate("mate", mate_decorator)
hof = tools.HallOfFame(HALL_OF_FAME)

def main():
    a = datetime.datetime.now()
    #random.seed(sys.argv[1])
    random.seed(1)

    CarregaFlor(PATH_BASE)
    # CarregaFloresExternas(PATH_BASE_EXTERNA)

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