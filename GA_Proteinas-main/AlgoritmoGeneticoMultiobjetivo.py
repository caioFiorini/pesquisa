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
from MOGAToolbox import MOGAToolbox
from FileManager import FileManager

# ====== MARK: Defining paths and file names ======
DATABASE_PATH = "BaseSting"
EXTERNAL_DATABASE_PATH = "BaseExterna"
EXTERNAL_DATABASE_FILE_NAME = "BaseExterna_Reduzida.csv"
CLASSIFIER_PATH = "Individuos/"

# TODO: uncomment when in final product
# FILE_NAME = sys.argv[1]

# TODO: comment when in final product
FILE_NAME = "TESTE"

CLASSIFIER_FILE_NAME = FILE_NAME + ".csv"

# ====== MARK: Algorithm's main parameters ======
# TODO: Uncomment when in production
# POPULATION_SIZE = int(sys.argv[2])
# GENERATION_COUNT = int(sys.argv[3])
# CROSSOVER = float(sys.argv[4])
# TOURNAMENT_SIZE = int(sys.argv[5])
# MUTATION_RATE = float(sys.argv[6])
# ELITISMO = int(sys.argv[7])

# TODO: Comment when in production
# POPULATION_SIZE = 500
POPULATION_SIZE = 20
TOURNAMENT_SIZE = 2  # NOT used in this file; check tsp.py or tspNovo.py
CROSSOVER = 0.7
MUTATION_RATE = 0.01
# GENERATION_COUNT = 100
GENERATION_COUNT = 5
ELITISMO = 1  # TODO: rename when find out what this is

HALL_OF_FAME_SIZE = 10
SAMPLE_COUNT = 490
TAMANHO_TRANSFORMADA = 10  # TODO: rename when find out what this is
INDIVIDUAL_SIZE = 104

PROTEIN_CLASSES_LIST = [
    "Hidrolases",
    "Isomerases",
    "Liases",
    "Ligases",
    "Oxidoredutases",
    "Transferases",
]

protein_matrix = []
external_protein_matrix = []


def setup_creator():
    # O creator cria uma nova classe com o nome passado no parâmetro
    # Em termos mais simples, essa linha de código cria uma nova classe de aptidão chamada FitnessMulti que tem dois componentes.
    # O primeiro componente é positivo e o segundo componente é negativo. A biblioteca Deap irá minimizar o segundo componente
    # da aptidão, o que significa maximizar o primeiro componente da aptidão.
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))

    # array.array -> é usado para criar um arranjo de tipos específicos.
    # no caso o Type code é i, logo ele cria um arranjo de inteiros
    # Ele cria um arranjo com os elementos do fitnes.
    creator.create(
        "Individual", array.array, typecode="i", fitness=creator.FitnessMulti
    )


def load_proteins(base_file_path: str):
    index = 0
    for class_number, protein_class in enumerate(PROTEIN_CLASSES_LIST):
        # Dentro de cada pasta de classe, tem um arquivo .txt com o nome da classe
        # e os arquivos .csv que devem ser lidos
        protein_list = FileManager.get_text_file_contents(base_file_path, protein_class)
        for protein in protein_list:
            with open(
                os.path.join(
                    base_file_path, protein_class, protein.rstrip("\n").rstrip("\r")
                ),
                "r",
            ) as csvfile:
                protein_reader = csv.reader(csvfile, delimiter=";")
                # Turning the protein_reader into a list helps later on when we want to use random access (check if we need it though).
                protein_matrix.insert(index, list(protein_reader))
                index = index + 1


def load_external_DB_proteins(base_file_path: str) -> None:
    with open(
        os.path.join(
            base_file_path, EXTERNAL_DATABASE_FILE_NAME.rstrip("\n").rstrip("\r")
        ),
        "r",
    ) as csvfile:
        protein_reader = csv.reader(csvfile, delimiter=";")
        # why insert at 0? SUS!
        external_protein_matrix.insert(0, list(protein_reader))


def count_individuals_relative_to_parent_average(population: list) -> (int, int):
    """_summary_ tem a finalidade de contar quantos indivíduos na população atual são considerados
    "piores" ou "melhores" em relação à sua aptidão em comparação com a média da aptidão de seus pais.

    Args:
        pop (list): lista de indivíduos.

    Returns:
    numPiores, numMelhores int: Quantos indivíduos na população atual são piores ou melhores em relação à média da aptidão de seus pais.
    """
    below_average_count = 0
    above_average_count = 0

    for individual in population:
        # still don't know why 0 and 1; can't rename to something better
        total_fitness0 = 0
        total_fitness1 = 0
        parent_count = 0

        for parent in individual.pais:
            parent_count += 1
            total_fitness0 += parent[0]
            total_fitness1 += parent[1]

        if parent_count > 0:
            average_fitness0 = total_fitness0 / parent_count
            average_fitness1 = total_fitness1 / parent_count

            if (
                individual.fitness.values[0] > average_fitness0
                and individual.fitness.values[1] <= average_fitness1
            ):
                above_average_count += 1
            else:
                below_average_count += 1
        individual.pais = []
    return below_average_count, above_average_count


def get_duplicate_individuals_count(population: list) -> int:
    """Count Duplicate Individuals.

    Args:
        population (list): A list of individuals in a specific population.

    Returns:
        int: Returns the count of duplicate individuals.
    """
    # When you create a set, it only allows unique elements
    unique_individuals = set()
    for i in range(len(population)):
        unique_individuals.add(tuple(population[i]))

    return len(population) - len(unique_individuals)


def main():
    start_time = time.time()

    setup_creator()
    evolution_toolbox = MOGAToolbox(
        INDIVIDUAL_SIZE,
        MUTATION_RATE,
        CLASSIFIER_FILE_NAME,
        CLASSIFIER_PATH,
        SAMPLE_COUNT,
        PROTEIN_CLASSES_LIST,
        TAMANHO_TRANSFORMADA,
        DATABASE_PATH,
        protein_matrix,
        external_protein_matrix,
    ).toolbox

    hall_of_fame = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # gera uma semente aleatória
    # random.seed(sys.argv[1])
    random.seed(1)

    print("Loading protein DB...")
    load_proteins(DATABASE_PATH)

    print("Loading external protein DB...")
    load_external_DB_proteins(EXTERNAL_DATABASE_PATH)

    # inicializa uma lista com os indivíduos da população
    population = evolution_toolbox.population(n=POPULATION_SIZE)

    for individual in population:
        # Inicializa uma lista vazia para os pais dos indivíduos.
        individual.pais = []

    for individual in population:
        # percorre cada indivíduo
        for i in range(0, INDIVIDUAL_SIZE):
            # Se o índice atual estiver entre os valores especificados no passo anterior, ele define
            # o valor no índice i do indivíduo p como 1.
            if i == 0 or i == 1 or i == 50 or i == 51 or i == 52 or i == 103:
                individual[i] = 1
            else:
                individual[i] = 0

    stats1 = tools.Statistics(lambda individual: individual.fitness.values)

    stats1.register("1) Media   ", numpy.mean, axis=0)
    stats1.register("2) Desvio Padrao   ", numpy.std, axis=0)
    stats1.register("3) Minimo  ", numpy.min, axis=0)
    stats1.register("4) Maximo  ", numpy.max, axis=0)

    stats2 = tools.Statistics(lambda individual: individual)
    stats2.register("Piores / Melhores  ", count_individuals_relative_to_parent_average)
    stats2.register("Ind. Repetidos	 ", get_duplicate_individuals_count)

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
    print("\n\nSetting up hall of fame...")
    best_individuals = open("melhores/" + FILE_NAME + ".txt", "a+")
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
