from deap import tools


class UnusedAlgorithmFunctions:
    def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
        """_summary_
            Faz a seleção dos melhores e aplica o torneio.
        Args:
            individuals (list): Uma lista de individuos.
            k (int): O número de indivíduos para seleção.
            frac_elitist (_type_): não sei (ainda)
            tournsize (int): O número de indivíduos participantes de cada torneio.

        Returns:
            _type_: retorna uma lista concatenada com a seleção dos melhores e a seleção do torneio.
        """
        return tools.selBest(individuals, int(k * frac_elitist)) + tools.selTournament(
            individuals, int(k * (1 - frac_elitist)), tournsize=tournsize
        )

    def get_best_attributes_from_individual(population):
        """_summary_ Retorna uma lista com as características do melhor indivíduo.

        Args:
            pop (list): Lista de indivíduos (popoulação).

        Returns:
            _type_: retorna uma lista com as características presentes no melhor indivíduo.
        """
        best_attributes = []
        fitness = 0
        for individual in population:
            if fitness < individual.fitness.values:
                best_attributes = individual
                fitness = individual.fitness.values

        # manda o indivíduo para receber somente as características.
        best_attributes = get_attributes_of_individual(best_attributes)
        return best_attributes

    def InicializaPopulacao(pop):
        """_summary_ Incia a população

        Args:
            pop (list): lista de indivíduos de uma determinada população
        """
        for p in pop:
            seed = random.randrange(1, 290)
            contador = 0
            for i in range(0, INDIVIDUAL_SIZE):
                valor = random.randint(0, 1)
                if seed == contador:
                    break

                if valor == 1:
                    p[i] = valor
                    contador = contador + 1
