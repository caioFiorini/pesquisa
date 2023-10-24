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
        return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)