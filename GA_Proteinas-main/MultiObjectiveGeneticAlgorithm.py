# Standard Library Imports
import datetime
import random

# Third-party Library Imports
from deap import tools

# Local Imports
from MOGATerminalLogger import MOGATerminalLogger
from classificadorT import ClassificadorT

class MultiObjectiveGeneticAlgorithm:

    def __init__(
        self,
        seed,
        population,
        evolution_toolbox,
        crossover_probability,
        mutation_probability,
        generation_count,
        population_size,
        diretorio,
        stats=None,
        hall_of_fame=None,
        verbose=__debug__,
        FILE_NAME="TESTE"
    ):
        self.population = population
        self.seed = seed
        self.evolution_toolbox = evolution_toolbox
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generation_count = generation_count
        self.population_size = population_size
        self.diretorio = diretorio
        self.stats = stats
        self.hall_of_fame = hall_of_fame
        self.verbose = verbose
        self.FILE_NAME = FILE_NAME

    def remove_individuals_with_zero_fitness_and_adjust_population(
        self, population: list, original_population_size: int
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

    def apply_variation_crossover_mutation(
        self, population, evolution_toolbox, crossover_probability, mutation_probability
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

    def execute(self):
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
        clt = ClassificadorT()
        logbook = tools.Logbook()
        num_generation_atual = 0
        clt.set_num_geracao(num_generation_atual)
        # gen A geração atual
        # nevals número de avaliações
        # ele concatena a lista de gerações e números de avaliações com as colunas que estão dentro de stats.
        logbook.header = ["gen", "nevals"] + (self.stats.fields if self.stats else [])

        # Evaluate the individuals with an invalid fitness
        # Coloca todos os invíduos que o fitness não é válido em uma lista.
        invalid_individuals = [
            individual for individual in self.population if not individual.fitness.valid
        ]

        # Pelo que eu entendi fitnesses é uma lista que recebe uma lista onde o nosso map, ele está pegando cada
        # indivíduo do invalid_ind e avaliando no toolbox.evaluate; Com isso retorna uma lista com o fitness dos
        # invalid_ind.
        fitnesses = self.evolution_toolbox.map(
            self.evolution_toolbox.evaluate, invalid_individuals
        )
        # Nesse for ele está iterando em cada invalid_ind e está "atribuindo" a ele o valor do seu respectivo
        # fitness.
        for individual, fitness in zip(invalid_individuals, fitnesses):
            individual.fitness.values = fitness

        # Recebe a população sem os indivíduos com fitness igual a 0;
        self.population = (
            self.remove_individuals_with_zero_fitness_and_adjust_population(
                self.population, self.population_size
            )
        )

        # Atualiza o Hall da fama
        if self.hall_of_fame is not None:
            self.hall_of_fame.update(self.population)

        # stats.compile recebe os dados sobre os quais a estatística é coletada.
        record = self.stats.compile(self.population) if self.stats else {}
        # salva as estatísticas das gerações no logbook.
        logbook.record(gen=0, nevals=len(invalid_individuals), **record)
        MOGATerminalLogger.print_generation_results(0, len(self.population), record, self.diretorio, self.FILE_NAME)

        # if verbose:
        #     print(logbook.stream)

        # Aplica o operador de seleção do NSGA2 nos indivíduos da população.
        # Ele manda a população e o tamanho da população que seria os indivíduos
        # para selecionar.
        self.population = self.evolution_toolbox.select(
            self.population, self.population_size
        )

        # Begin the generational process
        for generation_number in range(1, self.generation_count + 1):
            num_generation_atual = generation_number
            clt.set_num_geracao(num_generation_atual)
            # Select the next generation individuals

            # Seleção do torneio baseada na dominância (D) entre dois indivíduos, caso os dois indivíduos
            # não interdominem a seleção é feita com base na distância de aglomeração (CD).
            # Obs: O comprimento da sequencia de individuos deve ser 4.
            offspring = tools.selTournamentDCD(self.population, len(self.population))

            # Aplica a mutação e o crossover na população.
            offspring = self.apply_variation_crossover_mutation(
                offspring,
                self.evolution_toolbox,
                self.crossover_probability,
                self.mutation_probability,
            )

            self.log_generation(generation_number)

            # Evaluate the individuals with an invalid fitness

            invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.evolution_toolbox.map(
                self.evolution_toolbox.evaluate, invalid_individuals
            )
            for individual, fitness in zip(invalid_individuals, fitnesses):
                individual.fitness.values = fitness

            offspring = self.remove_individuals_with_zero_fitness_and_adjust_population(
                offspring, self.population_size
            )

            # Update the hall of fame with the generated individuals
            if self.hall_of_fame is not None:
                self.hall_of_fame.update(offspring)

            # Select the next generation population
            self.population = self.evolution_toolbox.select(
                self.population + offspring, self.population_size
            )

            # Append the current generation statistics to the logbook
            record = self.stats.compile(self.population) if self.stats else {}
            logbook.record(
                gen=generation_number, nevals=len(invalid_individuals), **record
            )

            MOGATerminalLogger.print_generation_results(
                generation_number, len(self.population), record, self.diretorio, self.FILE_NAME
            )
            # if verbose:
            #    print logbook.stream

        # para printar o que tem dentro do logbook;
        # for record in logbook:
        #     print(record)

        return self.population, logbook

    def log_generation(self, generation_number):
        GENERATION_LOG = open("log/Geracao_" + self.FILE_NAME + ".txt", "a+")
        GENERATION_LOG.write(
            "Classificando geracao: "
            + generation_number.__str__()
            + " Hora: "
            + datetime.datetime.now().__str__()
            + "\n"
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