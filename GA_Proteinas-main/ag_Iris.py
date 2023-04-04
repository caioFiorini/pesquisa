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
TAMANHO_TRANSFORMADA = 10

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

            if f.fitness.values[0] > media0 and f.fitness.values[1] <= media1
                numPiores += 1
            else:
                numPiores += 1
        f.pais = []
    return numePiores, numMelhores

def contaIndividuosIguais(pop):
    
