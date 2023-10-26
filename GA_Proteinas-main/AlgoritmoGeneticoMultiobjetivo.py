# Standard Library Imports
import array
import csv
import datetime
import os
import random
import time

# Third-party Library Imports
import numpy
from deap import base, creator, tools

# Local Imports
from Classificador import Classificador
from IOArquivo import FileReader

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
# TODO: Comment when in production
SAMPLE_COUNT = 490
TAMANHO_TRANSFORMADA = 10  # TODO: rename when find out what this is
INDIVIDUAL_SIZE = 104
# POPULATION_SIZE = 500
POPULATION_SIZE = 20
TOURNAMENT_SIZE = 2  # NOT used in this file; check tsp.py or tspNovo.py
CROSSOVER = 0.7
MUTATION_RATE = 0.01
# GENERATION_COUNT = 100
GENERATION_COUNT = 5
HALL_OF_FAME_SIZE = 10
ELITISMO = 1

# TODO: Uncomment when in production
# POPULACAO = int(sys.argv[2])
# CROSSOVER=float(sys.argv[4])
# GERACOES=int(sys.argv[3])
# TAXA_MUTACAO = float(sys.argv[6])
# TORNEIO=int(sys.argv[5])
# HALL_OF_FAME = 10
# ELITISMO = int(sys.argv[7])

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
    tamanho = (
        attributes_of_individual.__len__() + external_attributes_of_individual.__len__()
    )
    return fitness, tamanho


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
    file_reader = FileReader(SAMPLE_COUNT, PROTEIN_CLASSES_LIST, TAMANHO_TRANSFORMADA)
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


def get_text_file_contents(base_path: str, protein_class: str):
    file_path = os.path.join(base_path, protein_class, protein_class + ".txt")
    text_file = open(file_path, "r")
    return text_file


def load_proteins(base_file_path: str):
    index = 0
    for class_number, protein_class in enumerate(PROTEIN_CLASSES_LIST):
        # Dentro de cada pasta de classe, tem um arquivo .txt com o nome da classe
        # e os arquivos .csv que devem ser lidos
        protein_list = get_text_file_contents(base_file_path, protein_class)
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


def remove_individuals_with_zero_fitness_and_adjust_population(
    population: list, original_population_size: int
):
    """_summary_
    Essa função parece ter como objetivo remover indivíduos da população cujo
    segundo valor de aptidão seja igual a zero e, em seguida, preencher a população com cópias
    dos indivíduos existentes até que o tamanho original seja restaurado.

    Args:
        pop (list): lista de individuos
        tamanhoOriginal (int): tamanho da população

    Returns:
        list: Uma lista de indivíduos.
    """
    for individual in population:
        if individual.fitness.values[1] == 0:
            population.remove(individual)

    while original_population_size != len(population):
        seed = random.randrange(0, len(population) - 1)
        copy_of_individual = population[seed]
        population.insert(len(population), copy_of_individual)
    return population


def print_results(generation_count: int, population_size: int, record):
    print("\n\n")
    saida = (
        "Número da geração: "
        + generation_count.__str__()
        + "\n"
        + "Tamanho da população: "
        + population_size.__str__()
        + "\n"
        + "Total de filhos repetidos: "
        + record["Filhos"]["Ind. Repetidos\t "].__str__()
        + "\n"
        + "(Filhos abaixo da média, Filhos acima da média) = "
        + record["Filhos"]["Piores / Melhores  "].__str__()
        + "\n"
        + "1) Media  "
        + record["Fitness"]["1) Media   "][0].__str__()
        + "\n"
        + "1) Media  "
        + record["Fitness"]["1) Media   "][1].__str__()
        + "\n"
        + "2) Desvio Padrao "
        + record["Fitness"]["2) Desvio Padrao   "][0].__str__()
        + "\n"
        + "2) Desvio Padrao "
        + record["Fitness"]["2) Desvio Padrao   "][1].__str__()
        + "\n"
        + "3) Minimo "
        + record["Fitness"]["3) Minimo  "][0].__str__()
        + "\n"
        + "3) Minimo "
        + record["Fitness"]["3) Minimo  "][1].__str__()
        + "\n"
        + "4) Maximo "
        + record["Fitness"]["4) Maximo  "][0].__str__()
        + "\n"
        + "4) Maximo "
        + record["Fitness"]["4) Maximo  "][1].__str__()
    )

    print(saida)


def execute_multi_objective_evolutionary_algorithm(
    population,
    evolution_toolbox,
    crossover_probability,
    mutation_probability,
    generation_count,
    population_size,
    stats=None,
    hall_of_fame=None,
    verbose=__debug__,
):
    """_summary_
        É nessa função onde a mágica acontece, a ideia é que todo o processo de evolução das gerações aconteça aqui.

    Args:
        population (list): Uma lista com vários invíduos
        toolbox (): objeto da biblioteca deap
        cxpb (_type_): crossover (A probabilidade de acasalar dois indivíduos)
        mutpb (_type_): A taxa de mutação de um indivíduo
        ngen (_type_): número de gerações
        TAMANHO_POPULACAO (_type_): número da população
        stats (_type_, optional): Serve para guardar as métricas de cada geração.
        halloffame (_type_, optional): o hall da fama seria os 10 melhores indivíduos de cada
        verbose (_type_, optional): Se deve ou não registrar as estatísticas.

    Returns:
        _type_: _description_
    """
    logbook = tools.Logbook()

    # gen A geração atual
    # nevals número de avaliações
    # ele concatena a lista de gerações e números de avaliações com as colunas que estão dentro de stats.
    logbook.header = ["gen", "nevals"] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    # Coloca todos os invíduos que o fitness não é válido em uma lista.
    invalid_individuals = [
        individual for individual in population if not individual.fitness.valid
    ]

    # Pelo que eu entendi fitnesses é uma lista que recebe uma lista onde o nosso map, ele está pegando cada
    # indivíduo do invalid_ind e avaliando no toolbox.evaluate; Com isso retorna uma lista com o fitness dos
    # invalid_ind.
    fitnesses = evolution_toolbox.map(evolution_toolbox.evaluate, invalid_individuals)
    # Nesse for ele está iterando em cada invalid_ind e está "atribuindo" a ele o valor do seu respectivo
    # fitness.
    for individual, fitness in zip(invalid_individuals, fitnesses):
        individual.fitness.values = fitness

    # Recebe a população sem os indivíduos com fitness igual a 0;
    population = remove_individuals_with_zero_fitness_and_adjust_population(
        population, population_size
    )

    # Atualiza o Hall da fama
    if hall_of_fame is not None:
        hall_of_fame.update(population)

    # stats.compile recebe os dados sobre os quais a estatística é coletada.
    record = stats.compile(population) if stats else {}
    # salva as estatísticas das gerações no logbook.
    logbook.record(gen=0, nevals=len(invalid_individuals), **record)
    print_results(0, len(population), record)

    # if verbose:
    #     print(logbook.stream)

    # Aplica o operador de seleção do NSGA2 nos indivíduos da população.
    # Ele manda a população e o tamanho da população que seria os indivíduos
    # para selecionar.
    population = evolution_toolbox.select(population, population_size)

    # Begin the generational process
    for generation_number in range(1, generation_count + 1):
        # Select the next generation individuals

        # offspring = toolbox.select(population, len(population))

        # Seleção do torneio baseada na dominância (D) entre dois indivíduos, caso os dois indivíduos
        # não interdominem a seleção é feita com base na distância de aglomeração (CD).
        # Obs: O comprimento da sequencia de individuos deve ser 4.
        offspring = tools.selTournamentDCD(population, len(population))

        # Aplica a mutação e o crossover na população.
        offspring = apply_variation_crossover_mutation(
            offspring, evolution_toolbox, crossover_probability, mutation_probability
        )

        # Abre o arquivo de log.
        LOG_GERACOES = open("log/Geracao_" + FILE_NAME + ".txt", "a+")
        LOG_GERACOES.write(
            "Classificando geracao: "
            + generation_number.__str__()
            + " Hora: "
            + datetime.datetime.now().__str__()
            + "\n"
        )

        # Evaluate the individuals with an invalid fitness

        invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = evolution_toolbox.map(
            evolution_toolbox.evaluate, invalid_individuals
        )
        for individual, fitness in zip(invalid_individuals, fitnesses):
            individual.fitness.values = fitness

        offspring = remove_individuals_with_zero_fitness_and_adjust_population(
            offspring, population_size
        )

        # Update the hall of fame with the generated individuals
        if hall_of_fame is not None:
            hall_of_fame.update(offspring)

        # Select the next generation population
        population = evolution_toolbox.select(population + offspring, population_size)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=generation_number, nevals=len(invalid_individuals), **record)
        print_results(generation_number, len(population), record)
        # if verbose:
        #    print logbook.stream

    # para printar o que tem dentro do logbook;
    # for record in logbook:
    #     print(record)

    return population, logbook


def apply_variation_crossover_mutation(
    population, evolution_toolbox, crossover_probability, mutation_probability
):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their parents.

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
    offspring = [evolution_toolbox.clone(individual) for individual in population]

    # Apply crossover
    for i in range(1, len(offspring), 2):
        if random.random() < crossover_probability:
            offspring[i - 1], offspring[i] = evolution_toolbox.mate(
                offspring[i - 1], offspring[i]
            )
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    # Apply mutation
    for i in range(len(offspring)):
        if random.random() < mutation_probability:
            (offspring[i],) = evolution_toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


# O creator cria uma nova classe com o nome passado no parâmetro
# Em termos mais simples, essa linha de código cria uma nova classe de aptidão chamada FitnessMulti que tem dois componentes.
# O primeiro componente é positivo e o segundo componente é negativo. A biblioteca Deap irá minimizar o segundo componente
# da aptidão, o que significa maximizar o primeiro componente da aptidão.
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))

# array.array -> é usado para criar um arranjo de tipos específicos.
# no caso o Type code é i, logo ele cria um arranjo de inteiros
# Ele cria um arranjo com os elementos do fitnes.
creator.create("Individual", array.array, typecode="i", fitness=creator.FitnessMulti)

# Attribute generator
toolbox = base.Toolbox()

# O método register registra uma função na biblioteca Deap com o nome passado e você pode fornecer argumentos padrão que serão passados ​​automaticamente
# ao chamar a função registrada. Argumentos fixos podem então ser substituídos no momento da chamada da função.

# Em específico essa função gera uma função que quando chamada ela gera números aleatórios entre 1 e 0;
toolbox.register("indices", random.randint, 0, 1)

# A função tools.initRepeat repete um procedimento uma quantidade específica de vezes, no caso abaixo
# seria a quantidade de vezes do IND_SIZE.
# Essa função registra um indivíduo e inicializa ele com 0s - 1s aleatórios e repete IND_SIZE vezes.
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.indices, INDIVIDUAL_SIZE
)

# Essa função registra uma função de colocar indivíduos em uma lista e repete toolbox.individual vezes
# (quantidade de indivíduos).
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operadores genetic
# registra uma função de seleção de indivíduo do NSGA2
toolbox.register("select", tools.selNSGA2)

# registra uma função que executa um cruzamento de dois pontos nos indivíduos da sequência de entrada
toolbox.register("mate", tools.cxTwoPoint)

# registra uma função que embaralhe os atributos do indivíduo de entrada e retorne o mutante.
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=MUTATION_RATE)

# registra a função criada evaluate na biblioteca Deap
toolbox.register("evaluate", evaluate_fitness_of_individual)

# faz o cruzemento entre pais, gera os filhos e armazena pai e filho juntos
toolbox.decorate("mate", mate_and_get_mating_info)

hall_of_fame = tools.HallOfFame(HALL_OF_FAME_SIZE)
# toolbox.register("map", dtm.map)


def main():
    start_time = time.time()

    # gera uma semente aleatória
    # random.seed(sys.argv[1])
    random.seed(1)

    print("Loading protein DB...")
    load_proteins(DATABASE_PATH)

    print("Loading external protein DB...")
    load_external_DB_proteins(EXTERNAL_DATABASE_PATH)

    # inicializa uma lista com os indivíduos da população
    population = toolbox.population(n=POPULATION_SIZE)

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
    execute_multi_objective_evolutionary_algorithm(
        population,
        toolbox,
        CROSSOVER,
        MUTATION_RATE,
        GENERATION_COUNT,
        POPULATION_SIZE,
        stats=stats,
        hall_of_fame=hall_of_fame,
    )

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
