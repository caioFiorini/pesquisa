# Standard Library Imports
import array
import csv
import os
import random
import time
import sys

# Third-party Library Imports
import numpy
from deap import base, creator, tools

# Local Imports
from MultiObjectiveGeneticAlgorithm import MultiObjectiveGeneticAlgorithm
from MOGAToolbox import MOGAToolbox as mt
from FileManager import FileManager
from Arquivo import Arquivo
from algoritmo_Genetico import Algoritmo_Genetico
from algoritmos_ML import AlgoritmosML

# ====== MARK: Defining paths and file names ======
CLASSIFIER_PATH = "Individuos/"

# uncomment when in final product
FILE_NAME = sys.argv[1]

# comment when in final product
# FILE_NAME = "Iris"

CLASSIFIER_FILE_NAME = FILE_NAME + ".csv"

# ====== MARK: Algorithm's main parameters ======
HALL_OF_FAME_SIZE = 10
SEED = int(sys.argv[1])
POPULATION_SIZE = int(sys.argv[2])
GENERATION_COUNT = int(sys.argv[3])
CROSSOVER = float(sys.argv[4])
TAMANHO_TRANSFORMADA = int(sys.argv[5])
MUTATION_RATE = float(sys.argv[6])
ELITISMO = int(sys.argv[7])
DIRETORIO_EXPERIMENTO = sys.argv[9]

# POPULATION_SIZE = 16
# GENERATION_COUNT = 20
# CROSSOVER = 0.7
# TAMANHO_TRANSFORMADA = 10 
# MUTATION_RATE = 0.2
# ELITISMO = 1  

def main():
    start_time = time.time()
    
    arquivo = Arquivo()
    arquivo.le_arquivo("Iris.csv")
    
    SAMPLE_COUNT = arquivo.quantidade_linhas_colunas(0)
    INDIVIDUAL_SIZE = arquivo.quantidade_linhas_colunas(1)
    INDIVIDUAL_SIZE = INDIVIDUAL_SIZE-1
    mt.setup_creator()

    # escolher o algoritmo de machine learning
    algoritmo_ml = AlgoritmosML.KNN()
    
    evolution_toolbox = mt(
        INDIVIDUAL_SIZE,
        MUTATION_RATE,
        CLASSIFIER_FILE_NAME,
        CLASSIFIER_PATH,
        SAMPLE_COUNT,
        TAMANHO_TRANSFORMADA,
        arquivo,
        algoritmo_ml,
        SEED.__str__(),
        DIRETORIO_EXPERIMENTO
    ).toolbox

    hall_of_fame = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # gera uma semente aleatória
    random.seed(SEED)
    # random.seed(1)

    # inicializa uma lista com os indivíduos da população
    population = evolution_toolbox.population(n=POPULATION_SIZE)

    # Inicializa uma lista vazia para os pais dos indivíduos.
    for individual in population:
        individual.pais = []

    stats1 = tools.Statistics(lambda individual: individual.fitness.values)

    stats1.register("1) Media   ", numpy.mean, axis=0)
    stats1.register("2) Desvio Padrao   ", numpy.std, axis=0)
    stats1.register("3) Minimo  ", numpy.min, axis=0)
    stats1.register("4) Maximo  ", numpy.max, axis=0)

    stats2 = tools.Statistics(lambda individual: individual)
    stats2.register("Piores / Melhores  ", Algoritmo_Genetico.count_individuals_relative_to_parent_average)
    stats2.register("Ind. Repetidos	 ", Algoritmo_Genetico.get_duplicate_individuals_count)

    stats = tools.MultiStatistics(Fitness=stats1, Filhos=stats2)

    print("Starting algorithm...")
    multi_objective_genetic_algorithm = MultiObjectiveGeneticAlgorithm(
        population,
        evolution_toolbox,
        CROSSOVER,
        MUTATION_RATE,
        GENERATION_COUNT,
        POPULATION_SIZE,
        stats=stats,
        hall_of_fame=hall_of_fame,
        FILE_NAME=FILE_NAME,
    )

    multi_objective_genetic_algorithm.execute()

    # guarda os melhores e escreve no arquivo.
    # print("\n\nSetting up hall of fame...")
    best_individuals = open(DIRETORIO_EXPERIMENTO + "Melhores_" + FILE_NAME + ".txt", "w")
    best_individuals.write("\nHALL OF FAME:")
    for top_individual in hall_of_fame:
        best_individuals.write(
            top_individual.__str__() + top_individual.fitness.values.__str__() + "\n"
        )

    print("\nDone!")

    duration = time.time() - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(
        f"Total execution time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds."
    )


if __name__ == "__main__":
    main()
