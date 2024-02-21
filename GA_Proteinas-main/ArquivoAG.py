from MultiObjectiveGeneticAlgorithm import MultiObjectiveGeneticAlgorithm
from MOGAToolbox import MOGAToolbox
from FileManager import FileManager
from Arquivo import Arquivo
from deap import base, creator, tools
import array

class Algoritmo_Genetico:
    def __init__(self, 
                 population,
                 evolution_toolbox,
                 CROSSOVER,
                 MUTATION_RATE,
                 GENERATION_COUNT,
                 POPULATION_SIZE,
                 FILE_NAME,
                 stats=None,
                 hall_of_fame=None, 
                ):
        self.AG = MultiObjectiveGeneticAlgorithm(population, 
                                            evolution_toolbox, 
                                            CROSSOVER,
                                            MUTATION_RATE,
                                            GENERATION_COUNT,
                                            POPULATION_SIZE,
                                            FILE_NAME,
                                            stats,
                                            hall_of_fame, 
                                            verbose=__debug__)
        
        return self.AG
    
    def setup_creator(self):
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
    
    def count_individuals_relative_to_parent_average(population: list) -> (int, int):  # type: ignore
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