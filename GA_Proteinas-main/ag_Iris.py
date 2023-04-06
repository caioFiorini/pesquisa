import random 
import array
import datetime
import numpy
import csv
import os

from deap import base
from deap import creator
from deap import tools

from Classificador import Classificador
from IOArquivo import LeituraArquivo

NUMERO_AMOSTRAS = 151
TAMANHO_TRANSFORMADA = 2

LISTACLASSES = ["Iris-virginica", "Iris-setosa", "Iris-versicolor"]
PATH_BASE = "BaseSting"
NOME_ARQUIVO_EXTERNO = "BaseExterna_reduzida.csv"
PAHT_CLASSIFICADOR = "Individuos/"

nomeArquivo = 'TESTE'
NOME_ARQUIVO_CLASSIFICADOR = nomeArquivo + ".csv"
MATRIZ_FLORES = []
MATRIZ_FLORES_EXTERNAS = []

def evaluate(individual):
    listaCaracteristicas = Retornacaracteristica(individual)
    listaCaracteristicasExternas = RetornaCaracteristicaExternas(individual)
    MontarArquivoSVM(listaCaracteristicas, listaCaracteristicasExternas)
    fitness = ClassificadorCaracteristica(listaCaracteristicas)

    tamanho = litaCaracteristicas._len_() + listaCaracteristicasExternas._len_()
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
    ARQUIVO = open("Individuos/" + NOME_ARQUIVO_CLASSIFICADOR, "W")
    leitor = LeituraArquivo(NUMERO_AMOSTRAS, LISTACLASSES, TAMANHO_TRANSFORMADA);
    leitor.BuildCSV(PATH_BASE, ARQUIVO, listaCaracteristicas, listaCaracteristicasExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS)
    ARQUIVO.close()
    return

def openTxt(path_Base, classe):
    caminho = os.path.join(path_Base, classe, classe + ".txt")
    arq = open(caminho, 'r')
    return arq

def CarregaFlor(path_Base):
    contador = 0
    for numeroclasse, classe in enumerate(LISTACLASSES):
        listaFlores = openTxt(path_Base, classe)

        for flores in listaFlores: 
            with open(os.path.join(path_Base, classe, flores.rstrip('\n').rstrip('\r')), 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                x = list(reader)
                MATRIZ_FLORES.insert(contador, x)
                contador = contador + 1

def carregaFloresExternas (path_Base):
    with open(os.path.join(path_Base, NOME_ARQUIVO_EXTERNO.rstrip('\n').rstrip('\n')), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        x = list(reader)
        MATRIZ_FLORES_EXTERNAS.insert(0, x)

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
    def wraper(ind1, ind2, *arg, **kerhs):
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
    logbook.header = ['gen', 'nevals'] + (Stats.fields if stats else [])

    #Evaluate the individuals with on invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolox.map(toolbox.evaluate, invalid_ind)
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
        #Seleciona a proxima geração de indiv´duos
        offspring = varAnd(offspring, toolbox, cxp, mutpb)

        LOG_GERACOES = open("log/Geracao_" + nomeArquivo + '.txt', "ta+")
        LOG_GERACOES.write('Classificando geracao: ' +  gen.__str__() + 'Hora: ' + datetime.datetime.now().__str__() + '\n')

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip (invalid_ind, fitnesses):
            ind.fitness.values = fit

        #Seleciona a próxima geração de populações
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
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offpring[i])

            del offspring[i-1].fitness.values, offspring[i].fitness.values
    
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

#Individuo and Operator genetic
IND_SIZE = 104
POPULACAO = 1