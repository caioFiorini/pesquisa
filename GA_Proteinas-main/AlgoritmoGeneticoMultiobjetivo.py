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
from Classificador import Classificador
from FileManager import FileManager

# ====== MARK: Defining paths and file names ======
DATABASE_PATH = "BaseSting"
EXTERNAL_DATABASE_PATH = "BaseExterna"
EXTERNAL_DATABASE_FILE_NAME = "BaseExterna_Reduzida.csv"
CLASSIFIER_PATH = "Individuos/"

# TODO: uncomment when in final product
FILE_NAME = sys.argv[1]

# TODO: comment when in final product
# FILE_NAME = "TESTE"

CLASSIFIER_FILE_NAME = FILE_NAME + ".csv"

# ====== MARK: Algorithm's main parameters ======
# TODO: Uncomment when in production
POPULATION_SIZE = int(sys.argv[2])
GENERATION_COUNT = int(sys.argv[3])
CROSSOVER = float(sys.argv[4])
TOURNAMENT_SIZE = int(sys.argv[5])
MUTATION_RATE = float(sys.argv[6])
ELITISMO = int(sys.argv[7])

# TODO: Comment when in production
# POPULATION_SIZE = 500
# TOURNAMENT_SIZE = 2  # NOT used in this file; check tsp.py or tspNovo.py
# CROSSOVER = 0.7
# MUTATION_RATE = 0.01
# GENERATION_COUNT = 100
# ELITISMO = 1 # TODO: rename when find out what this is

HALL_OF_FAME_SIZE = 10
SAMPLE_COUNT = 500
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
    creator.create("Individual", array.array, typecode="i", fitness=creator.FitnessMulti)
    
def setup_and_get_evolution_toolbox():
    # Attribute generator
    evolution_toolbox = base.Toolbox()

    # O método register registra uma função na biblioteca Deap com o nome passado e você pode fornecer argumentos padrão que serão passados ​​automaticamente
    # ao chamar a função registrada. Argumentos fixos podem então ser substituídos no momento da chamada da função.

    # Em específico essa função gera uma função que quando chamada ela gera números aleatórios entre 1 e 0;
    evolution_toolbox.register("indices", random.randint, 0, 1)

    # A função tools.initRepeat repete um procedimento uma quantidade específica de vezes, no caso abaixo
    # seria a quantidade de vezes do IND_SIZE.
    # Essa função registra um indivíduo e inicializa ele com 0s - 1s aleatórios e repete IND_SIZE vezes.
    evolution_toolbox.register(
        "individual", tools.initRepeat, creator.Individual, evolution_toolbox.indices, INDIVIDUAL_SIZE
    )

    # Essa função registra uma função de colocar indivíduos em uma lista e repete toolbox.individual vezes
    # (quantidade de indivíduos).
    evolution_toolbox.register("population", tools.initRepeat, list, evolution_toolbox.individual)

    # Operadores genetic
    # registra uma função de seleção de indivíduo do NSGA2
    evolution_toolbox.register("select", tools.selNSGA2)

    # registra uma função que executa um cruzamento de dois pontos nos indivíduos da sequência de entrada
    evolution_toolbox.register("mate", tools.cxTwoPoint)

    # registra uma função que embaralhe os atributos do indivíduo de entrada e retorne o mutante.
    evolution_toolbox.register("mutate", tools.mutShuffleIndexes, indpb=MUTATION_RATE)

    # registra a função criada evaluate na biblioteca Deap
    evolution_toolbox.register("evaluate", evaluate_fitness_of_individual)

    # faz o cruzemento entre pais, gera os filhos e armazena pai e filho juntos
    evolution_toolbox.decorate("mate", mate_and_get_mating_info)
    # toolbox.register("map", dtm.map)
    
    return evolution_toolbox
    
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

def evaluate_fitness_of_individual(individual) -> (numpy.float64, int):
    """Essa função retorna o fitness do indivíduo.

    Args:
        individual : creator.Individual
            indivíduos da população.

    Returns:
        (float64, int)
            o fitness para o indivíduo e a quantidade de características.
    """
    # dentro do cromossomo temos as características presentes no indivíduos [0,1,0,1,0,1]
    # ele pega esses atributos e dentro de um svm ele testa para ver a qualidade dele.
    attributes_of_individual = get_attributes_of_individual(individual)
    external_attributes_of_individual = get_external_DB_attributes_of_individual(
        individual
    )
    create_SVM_file(attributes_of_individual, external_attributes_of_individual)
    fitness = get_fitness_of_individual(attributes_of_individual)
    # check whether this comment is really useful or not
    # fitness = 1 - fitness
    individual_size = (
        attributes_of_individual.__len__() + external_attributes_of_individual.__len__()
    )
    return fitness, individual_size


def get_attributes_of_individual(individual) -> [str]:
    """Lista as características (atributos) de um indivíduo.

    Args:
        individual : deap.creator.Individual
            o indivíduo. (cromossomo [0,0,1,0,...]).

    Returns:
        [str]
            lista com as caracterísitcas do indivíduo.
    """
    attributes = []
    attribute_count = 0
    for attribute in individual:
        if attribute_count >= 50:
            return attributes
        # WARNING: check with everyone (returns array with two items) -> [0, 1]
        if attribute == 1:
            attributes.append(attribute_count)  # why?
        attribute_count += 1
    return attributes


def get_external_DB_attributes_of_individual(individual) -> [str]:
    """Lista as características das bases externas de enriquecimento da base principal.

    Args:
        individual : deap.creator.Individual
            o indivíduo. (cromossomo [0,0,1,0,...]).

    Returns:
        [str]
            retorna uma lista com as características externas
    """
    attributes = []
    attribute_count = 0
    # WARNING: improve ASAP
    for attribute in individual:
        if attribute_count >= 51 and attribute == 1:
            value = attribute_count - 51
            attributes.append(value)  # why?
        attribute_count += 1
    return attributes


def create_SVM_file(
    attributes_of_individual: [str], external_attributes_of_individual: [str]
):
    """_summary_ Gera um arquivo igual uma base de dados para testar na svm

    Args:
        attributes_of_individual : [str]
            Quantidade listada de características, igual quando faz leitura em um csv

        external_attributes_of_individual : [str]
            Quantidade listada de características, igual quando faz leitura em um csv
    """
    SVM_FILE = open("Individuos/" + CLASSIFIER_FILE_NAME, "w")
    file_reader = FileManager(SAMPLE_COUNT, PROTEIN_CLASSES_LIST, TAMANHO_TRANSFORMADA)
    file_reader.BuildCSV(
        DATABASE_PATH,
        SVM_FILE,
        attributes_of_individual,
        external_attributes_of_individual,
        protein_matrix,
        external_protein_matrix,
    )
    SVM_FILE.close()
    return

def get_fitness_of_individual(attribute_list: [int]) -> numpy.float64:
    """_summary_ Recebe uma lista de caracteristicas de apenas 1 indivíduo.

    Args:
        listaCaracteristicas (_type_): lista com 0s e 1s [0,1,0,1] -> Cromossomo.

    Returns:
        _type_: Como o fitness no trabalho do Bruno é baseado no fmeasure ele retorna o fmeasure.
    """

    if not attribute_list:
        return 0
    svm = Classificador(CLASSIFIER_PATH, CLASSIFIER_FILE_NAME)
    # check which function we are really using and remove the comment
    # resultPrecision = svm.fitness()
    _FMeasure_result = svm.fitness1()
    return _FMeasure_result


# Em termos simples, o decorador mate_decorator() permite que você armazene os pais dos filhos gerados
# por um cruzamento. Isso pode ser útil para fins de depuração ou para rastrear a evolução de uma
# população ao longo do tempo.
def mate_and_get_mating_info(mating_function: callable) -> callable:
    def wrapper(parent_1, parent_2, *args, **kwargs):
        parent_fitness_values = []
        for parent in (parent_1, parent_2):
            parent_fitness_values.append(parent.fitness.values)
        offspring = mating_function(parent_1, parent_2, *args, **kwargs)
        result = offspring
        for child in offspring:
            child.parents = parent_fitness_values
        return result

    return wrapper


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
    evolution_toolbox = setup_and_get_evolution_toolbox()

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
        FILE_NAME=FILE_NAME
    )

    multi_objective_genetic_algorithm.execute()
   
    # guarda os melhores e escreve no arquivo.
    print("\n\nSetting up hall of fame...")
    best_individuals = open("melhores/" + FILE_NAME + ".txt", "a+")
    best_individuals.write("\nHALL OF FAME:")
    for top_individual in hall_of_fame:
        best_individuals.write(top_individual.__str__() + top_individual.fitness.values.__str__() + "\n")

    print("\nDone!")
    
    duration = time.time() - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"Total execution time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds.")

if __name__ == "__main__":
    main()
