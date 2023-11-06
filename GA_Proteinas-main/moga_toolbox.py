# Standard Library Imports
import random

# Third-party Library Imports
import numpy
from deap import base, creator, tools

# Local Imports
from svm_classifier import SVMClassifier
from file_manager import FileManager


class MOGAToolbox:
    def __init__(
        self,
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
    ) -> None:
        self.__INDIVIDUAL_SIZE = INDIVIDUAL_SIZE
        self.__MUTATION_RATE = MUTATION_RATE
        self.__CLASSIFIER_FILE_NAME = CLASSIFIER_FILE_NAME
        self.__CLASSIFIER_PATH = CLASSIFIER_PATH
        self.__SAMPLE_COUNT = SAMPLE_COUNT
        self.__PROTEIN_CLASSES_LIST = PROTEIN_CLASSES_LIST
        self.__TAMANHO_TRANSFORMADA = TAMANHO_TRANSFORMADA
        self.__DATABASE_PATH = DATABASE_PATH
        self.__protein_matrix = protein_matrix
        self.__external_protein_matrix = external_protein_matrix
        self.toolbox = self.__setup_and_get_MOGA_toolbox()

    def __evaluate_fitness_of_individual(self, individual) -> (numpy.float64, int):
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
        attributes_of_individual = self.__get_internal_DB_attributes_of_individual(
            individual
        )
        external_attributes_of_individual = (
            self.__get_external_DB_attributes_of_individual(individual)
        )
        self.__create_SVM_file(
            attributes_of_individual, external_attributes_of_individual
        )
        fitness = self.__get_fitness_of_individual(attributes_of_individual)
        # check whether this comment is really useful or not
        # fitness = 1 - fitness
        individual_size = (
            attributes_of_individual.__len__()
            + external_attributes_of_individual.__len__()
        )
        return fitness, individual_size

    def __get_internal_DB_attributes_of_individual(self, individual) -> [str]:
        """Lista as características (atributos) de um indivíduo.

        Args:
            individual : deap.creator.Individual
                o indivíduo. (cromossomo [0,0,1,0,...]).

        Returns:
            [str]
                lista com as caracterísitcas do indivíduo.
        """
        return [
            index for index, attribute in enumerate(individual[:50]) if attribute == 1
        ]

    def __get_external_DB_attributes_of_individual(self, individual) -> [str]:
        """Lista as características das bases externas de enriquecimento da base principal.

        Args:
            individual : deap.creator.Individual
                o indivíduo. (cromossomo [0,0,1,0,...]).

        Returns:
            [str]
                retorna uma lista com as características externas
        """
        return [
            index for index, attribute in enumerate(individual[51:]) if attribute == 1
        ]

    # Em termos simples, o decorador mate_decorator() permite que você armazene os pais dos filhos gerados
    # por um cruzamento. Isso pode ser útil para fins de depuração ou para rastrear a evolução de uma
    # população ao longo do tempo.
    def __mate_and_get_mating_info(self, mating_function: callable) -> callable:
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

    def __setup_and_get_MOGA_toolbox(self):
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
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.indices,
            self.__INDIVIDUAL_SIZE,
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
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=self.__MUTATION_RATE)

        # registra a função criada evaluate na biblioteca Deap
        toolbox.register("evaluate", self.__evaluate_fitness_of_individual)

        # faz o cruzemento entre pais, gera os filhos e armazena pai e filho juntos
        toolbox.decorate("mate", self.__mate_and_get_mating_info)

        return toolbox

    def __get_fitness_of_individual(self, attribute_list: [int]) -> numpy.float64:
        """_summary_ Recebe uma lista de caracteristicas de apenas 1 indivíduo.

        Args:
            listaCaracteristicas (_type_): lista com 0s e 1s [0,1,0,1] -> Cromossomo.

        Returns:
            _type_: Como o fitness no trabalho do Bruno é baseado no fmeasure ele retorna o fmeasure.
        """

        if not attribute_list:
            return 0
        svm = SVMClassifier(self.__CLASSIFIER_PATH, self.__CLASSIFIER_FILE_NAME)
        # check which function we are really using and remove the comment
        # resultPrecision = svm.fitness()
        _FMeasure_result = svm.fitness1()
        return _FMeasure_result

    def __create_SVM_file(
        self, attributes_of_individual: [str], external_attributes_of_individual: [str]
    ):
        """_summary_ Gera um arquivo igual uma base de dados para testar na svm

        Args:
            attributes_of_individual : [str]
                Quantidade listada de características, igual quando faz leitura em um csv

            external_attributes_of_individual : [str]
                Quantidade listada de características, igual quando faz leitura em um csv
        """
        SVM_FILE = open("Individuos/" + self.__CLASSIFIER_FILE_NAME, "w")
        file_reader = FileManager(
            self.__SAMPLE_COUNT,
            self.__PROTEIN_CLASSES_LIST,
            self.__TAMANHO_TRANSFORMADA,
        )
        file_reader.BuildCSV(
            self.__DATABASE_PATH,
            SVM_FILE,
            attributes_of_individual,
            external_attributes_of_individual,
            self.__protein_matrix,
            self.__external_protein_matrix,
        )
        SVM_FILE.close()
        return
