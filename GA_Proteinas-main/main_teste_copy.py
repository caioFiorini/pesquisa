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
# from MultiObjectiveGeneticAlgorithm import MultiObjectiveGeneticAlgorithm
from MOGAToolbox import MOGAToolbox as mt
# from FileManager import FileManager
from Arquivo import Arquivo
# from algoritmo_Genetico import Algoritmo_Genetico
from algoritmos_ML import AlgoritmosML as am

# ====== MARK: Defining paths and file names ======
CLASSIFIER_PATH = "Individuos/"
# FILE_NAME = sys.argv[1]
# CLASSIFIER_FILE_NAME = FILE_NAME + ".csv"

# ====== MARK: Algorithm's main parameters ======
# HALL_OF_FAME_SIZE = 10
# SEED = int(sys.argv[1])
# POPULATION_SIZE = int(sys.argv[2])
# GENERATION_COUNT = int(sys.argv[3])
# CROSSOVER = float(sys.argv[4])
# TAMANHO_TRANSFORMADA = int(sys.argv[5])
# MUTATION_RATE = float(sys.argv[6])
# ELITISMO = int(sys.argv[7])
# DIRETORIO_EXPERIMENTO = sys.argv[9]

# POPULATION_SIZE = 16
# GENERATION_COUNT = 20
# CROSSOVER = 0.7
# TAMANHO_TRANSFORMADA = 10 
# MUTATION_RATE = 0.2
# ELITISMO = 1  

def main():
    start_time = time.time()
    
    
    # Leitura dos arquivos
    arquivo = Arquivo()
    linhas_arquivo = arquivo.le_arquivo_teste()
    arquivo_csv = linhas_arquivo[0].strip("\n")
    arquivo.le_arquivo(arquivo_csv.strip())    
    SAMPLE_COUNT = arquivo.quantidade_linhas_colunas(0)
    INDIVIDUAL_SIZE = arquivo.quantidade_linhas_colunas(1)
    INDIVIDUAL_SIZE = INDIVIDUAL_SIZE-1
    mt.setup_creator()
        
    # Preparando os elementos para entrar no teste
    seed = linhas_arquivo[1].strip("\n").split(" ")
    seed.pop(0)
    Population = linhas_arquivo[2].strip("\n").split(" ")
    Generations = linhas_arquivo[3].strip("\n").split(" ")
    CrossOverFactor = linhas_arquivo[4].strip("\n").split(" ")
    TournamentSize = linhas_arquivo[5].strip("\n").split(" ")
    TournamentSize.pop(0)
    MutationRate = linhas_arquivo[6].strip("\n").split(" ")
    ElitismFactor = linhas_arquivo[7].strip("\n").split(" ")
    ElitismFactor.pop(0)
    algoritmo_ml = linhas_arquivo[8].strip("\n").split(" ")
    population_min = Population[1].strip()
    population_max = Population[2].strip()
    population_ite = Population[3].strip()
    generations_min = Generations[1].strip()
    generation_max = Generations[2].strip()
    generation_ite = Generations[3].strip()
    crossover_min = CrossOverFactor[1].strip()
    crossover_max = CrossOverFactor[2].strip()
    crossover_ite = CrossOverFactor[3].strip()
    mutation_min = MutationRate[1].strip()
    mutation_max = MutationRate[2].strip()
    mutation_ite = MutationRate[3].strip()
    
    print(algoritmo_ml[0])
    
    # For onde os testes irão acontecer, dentro dele acontecerá a criação das pastas e a escrita dos testes.
    # for i in seed:
    #     for j in range(population_min, population_max, population_ite):
    #         for k in range(generations_min, generation_max, generation_ite):
    #             for l in range(crossover_min, crossover_max, crossover_ite):
    #                 for m in range(mutation_min, mutation_max, mutation_ite):
                        
    
if __name__ == "__main__":
    main()
