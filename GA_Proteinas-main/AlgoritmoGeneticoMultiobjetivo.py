import random
import array
import datetime
import numpy
import sys
import csv
import os
import numpy
import copy
# import arrow

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
#from deap import dtm

from Classificador import Classificador
from IOArquivo import LeituraArquivo

NUMERO_AMOSTRAS = 490
TAMANHO_TRANSFORMADA = 10

LISTACLASSES = ["Hidrolases", "Isomerases", "Liases", "Ligases", "Oxidoredutases", "Transferases"]
PATH_BASE = "BaseSting"
PATH_BASE_EXTERNA = "BaseExterna"
NOME_ARQUIVO_EXTERNO = 'BaseExterna_Reduzida.csv'
PATH_CLASSIFICADOR = "Individuos/"
#nomeArquivo = sys.argv[1]
nomeArquivo = 'TESTE'
NOMEARQUIVO_CLASSIFICADOR = nomeArquivo + ".csv"
MATRIZ_PROTEINAS = []
MATRIZ_PROTEINAS_EXTERNAS = []

def evaluate(individual):
    """ Essa função retorna o fitness do indivíduo.

    Args:
        individual : indivíduos da população.

    Returns:
        o fitness para o indivíduo e a quantidade de características.
    """

    # dentro do cromosso temos as características presentes no indivíduos [0,1,0,1,0,1]
    # ele pega esses atributos e dentro de um svm ele testa para ver a qualidade dele.
    listaCaracteristicas = RetornaCaracteristica(individual)
    listaCaracteristicasExternas = RetornaCaracteristicaExternas(individual)
    MontaArquivoSVM(listaCaracteristicas, listaCaracteristicasExternas)
    fitness = ClassificadorCaracteristica(listaCaracteristicas)
    #fitness = 1 - fitness
    tamanho = listaCaracteristicas.__len__() + listaCaracteristicasExternas.__len__()
    return fitness, tamanho,

def RetornaCaracteristica(ind1):
    """Lista as características (atributos) de um indivíduo.

    Args:
        ind1: o indivíduo. (cromossomo [0,0,1,0,...]).

    Returns:
        List : retorna uma lista com as caracterísitcas.
    """
    caracteristicas = []
    x = 0
    for i in ind1:
        if(x >= 50):
            return caracteristicas
        if(i == 1):
            caracteristicas.append(x)
        x = x + 1
    return caracteristicas

def RetornaCaracteristicaExternas(ind1):
    """Lista as características das bases externas de enriquecimento da base principal.

    Args:
        ind1 (_type_): O individuos (cromossomo [0,0,1,0,...]).

    Returns:
        List : retorna uma lista com as características a mais. 
    """
    caracteristicas = []
    x = 0
    for i in ind1:
        if(x >= 51 and i == 1):
            valor = x - 51
            caracteristicas.append(valor)
        x = x + 1
    return caracteristicas



def MontaArquivoSVM(listaCaracteristicas, listaCaracteristicasExternas):
    """_summary_ Gera um arquivo igual uma base de dados para testar na svm

    Args:
        listaCaracteristicas (_type_): Quantidade listada de características, igual quando faz leitura em um csv
        listaCaracteristicasExternas (_type_): Quantidade listada de características, igual quando faz leitura em um csv
    """
    ARQUIVO = open("Individuos/" + NOMEARQUIVO_CLASSIFICADOR, "w")
    leitor = LeituraArquivo(NUMERO_AMOSTRAS, LISTACLASSES, TAMANHO_TRANSFORMADA)
    leitor.BuildCSV(PATH_BASE, ARQUIVO, listaCaracteristicas, listaCaracteristicasExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS)
    ARQUIVO.close()
    return

def openTxt(path_Base, classe):
    caminho = os.path.join(path_Base, classe, classe + ".txt")
    arq = open(caminho, 'r')
    return arq

def CarregaProteinas(path_Base):
    contador = 0
    for numeroclasse, classe in enumerate(LISTACLASSES): 

        # Dentro de cada pasta de classe, tem um arquivo .txt com o nome da classe
        # e os arquivos .csv que devem ser lidos
        listaProteinas = openTxt(path_Base, classe)
        # print(listaProteinas)

        for proteina in listaProteinas:
            with open(os.path.join(path_Base, classe, proteina.rstrip('\n').rstrip('\r')), 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                x = list(reader)
                MATRIZ_PROTEINAS.insert(contador, x)
                contador = contador + 1
        
        # print(MATRIZ_PROTEINAS)


def CarregaProteinasExternas(path_Base):
    with open(os.path.join(path_Base, NOME_ARQUIVO_EXTERNO.rstrip('\n').rstrip('\r')), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        x = list(reader)
        MATRIZ_PROTEINAS_EXTERNAS.insert(0, x)

# não é utilizada.
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

def ClassificadorCaracteristica(listaCaracteristicas):
    """_summary_ Recebe uma lista de caracteristicas de apenas 1 indivíduo.

    Args:
        listaCaracteristicas (_type_): lista com 0s e 1s [0,1,0,1] -> Cromossomo.

    Returns:
        _type_: Como o fitness no trabalho do Bruno é baseado no fmeasure ele retorna o fmeasure.
    """
    if(listaCaracteristicas.__len__() == 0):
        return 0
    svm = Classificador(PATH_CLASSIFICADOR, NOMEARQUIVO_CLASSIFICADOR)
    #resultPrecision = svm.fitness()
    resultFMeasure = svm.fitness1()
    return resultFMeasure

def Melhor(pop):
    """_summary_ Retorna uma lista com as características do melhor indivíduo.

    Args:
        pop (list): Lista de indivíduos (popoulação).

    Returns:
        _type_: retorna uma lista com as características presentes no melhore indivíduo.
    """
    melhor = []
    fitness = 0
    for p in pop:
        if(fitness < p.fitness.values):
            melhor = p
            fitness = p.fitness.values

    # manda o indivíduo para receber somente as características.
    melhor = RetornaCaracteristica(melhor)
    return melhor

# Em termos simples, o decorador mate_decorator() permite que você armazene os pais dos filhos gerados 
# por um cruzamento. Isso pode ser útil para fins de depuração ou para rastrear a evolução de uma 
# população ao longo do tempo.
def mate_decorator(func):
    def wraper(ind1, ind2, *args, **kargs):
        pais = []
        for p in (ind1, ind2):
            pais.append(p.fitness.values)
        # Esta linha chama a função de cruzamento original para gerar os filhos.
        filhos = func(ind1, ind2, *args, **kargs)
        ret = filhos
        for f in filhos:
            f.pais = pais
        # esse return eu não tenho certeza se está correto
        return ret
    return wraper

def contaFilhos(pop):
    """_summary_ tem a finalidade de contar quantos indivíduos na população atual são considerados 
    "piores" ou "melhores" em relação à sua aptidão em comparação com a média da aptidão de seus pais.

    Args:
        pop (list): lista de indivíduos.

    Returns:
       numPiores, numMelhores int: Quantos indivíduos na população atual são piores ou melhores em relação à média da aptidão de seus pais.
    """
    numPiores = 0
    numMelhores = 0
    for f in pop:
        tot0 = 0
        tot1 = 0
        count = 0
        for p in f.pais:
            count += 1
            tot0 += p[0]
            tot1 += p[1]
            # print p
        if count > 0:
            media0 = tot0 / count
            media1 = tot1 / count
            # print tot, count, media, f.value
            if f.fitness.values[0] > media0 and f.fitness.values[1] <= media1:
                numMelhores += 1
            else:
                numPiores += 1
        f.pais = []
    return numPiores, numMelhores

def contaIndividuosIguais(pop):
    """_summary_ 

    Args:
        pop (list): lista com os indivíduos de determinada população.

    Returns:
        _type_: retorna a quantidade de indivíduos iguais.
    """
    numRepetidos = 0
    # quando seta um conjunto, o conjunto só permite elementos iguais
    unicos = set()
    for i in range(len(pop)):
        unicos.add(tuple(pop[i]))
    return len(pop) - len(unicos)

# Aparenetemente esse função não é usada
def InicializaPopulacao(pop):
    """_summary_ Incia a população

    Args:
        pop (list): lista de indivíduos de uma determinada população
    """
    for p in pop:
        seed = random.randrange(1, 290)
        #print 'SEMENTE:', seed
        contador = 0
        for i in range(0, IND_SIZE):

            valor = random.randint(0, 1)
            if (seed == contador):
                break

            if (valor == 1):
                p[i] = valor
                contador = contador + 1


def RemoveRepoe(pop, tamanhoOriginal):
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
    for p in pop:
        # Remove indivíduos cujo o fitness é igual a 0.
        if (p.fitness.values[1] == 0):
            pop.remove(p)

    while (tamanhoOriginal != len(pop)):
        seed = random.randrange(0, len(pop) - 1)
        copia = pop[seed]
        pop.insert(len(pop), copia)
    return pop

def ImprimeSaida(ngen, populacao, record):
    print(populacao)
    print("\n\n")
    saida = ngen.__str__() + '\t' + len(populacao).__str__() + \
    '\t' + record['Filhos']['Ind. Repetidos\t '].__str__() + \
    '\n' + 'Piores / Melhores ' + record['Filhos']['Piores / Melhores  '].__str__() + \
    '\n' + '1) Media  ' + record['Fitness']['1) Media   '][0].__str__() + \
    '\n' + '1) Media  ' + record['Fitness']['1) Media   '][1].__str__() + \
    '\n' + '2) Desvio Padrao ' + record['Fitness']['2) Desvio Padrao   '][0].__str__() + \
    '\n' + '2) Desvio Padrao ' + record['Fitness']['2) Desvio Padrao   '][1].__str__() + \
    '\n' + '3) Minimo ' + record['Fitness']['3) Minimo  '][0].__str__() + \
    '\n' + '3) Minimo ' + record['Fitness']['3) Minimo  '][1].__str__() + \
    '\n' + '4) Maximo ' + record['Fitness']['4) Maximo  '][0].__str__() + \
    '\n' + '4) Maximo ' + record['Fitness']['4) Maximo  '][1].__str__()
            
    print (saida)

def eaMulti(population, toolbox, cxpb, mutpb, ngen, TAMANHO_POPULACAO, stats=None, halloffame=None, verbose=__debug__):
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
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    # Coloca todos os invíduos que o fitness não é válido em uma lista.
    invalid_ind = [ind for ind in population if not ind.fitness.valid]

    # Pelo que eu entendi fitnesses é uma lista que recebe uma lista onde o nosso map, ele está pegando cada
    # indivíduo do invalid_ind e avaliando no toolbox.evaluate; Com isso retorna uma lista com o fitness dos
    # invalid_ind.
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    # Nesse for ele está iterando em cada invalid_ind e está "atribuindo" a ele o valor do seu respectivo 
    # fitness.
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Recebe a população sem os indivíduos com fitness igual a 0;
    population = RemoveRepoe(population, TAMANHO_POPULACAO)

    # Atualiza o Hall da fama
    if halloffame is not None:
        halloffame.update(population)

    # stats.compile recebe os dados sobre os quais a estatística é coletada.
    record = stats.compile(population) if stats else {}
    # salva as estatísticas das gerações no logbook.
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    ImprimeSaida(0, population, record)

    # if verbose:
    #    print logbook.stream

    # Aplica o operador de seleção do NSGA2 nos indivíduos da população.
    # Ele manda a população e o tamanho da população que seria os indivíduos 
    # para selecionar.
    population = toolbox.select(population, TAMANHO_POPULACAO)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        
        # offspring = toolbox.select(population, len(population))


        # Seleção do torneio baseada na dominância (D) entre dois indivíduos, caso os dois indivíduos 
        # não interdominem a seleção é feita com base na distância de aglomeração (CD).
        # Obs: O comprimento da sequencia de individuos deve ser 4.
        offspring = tools.selTournamentDCD(population, len(population))

        # Aplica a mutação e o crossover na população.
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Abre o arquivo de log.
        LOG_GERACOES = open("log/Geracao_" + nomeArquivo + '.txt', "a+")
        LOG_GERACOES.write('Classificando geracao: ' + gen.__str__() + ' Hora: ' + datetime.datetime.now().__str__() + '\n')

        # Evaluate the individuals with an invalid fitness
        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        offspring = RemoveRepoe(offspring, TAMANHO_POPULACAO)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Select the next generation population
        population = toolbox.select(population + offspring, TAMANHO_POPULACAO)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        ImprimeSaida(gen, population, record)
        #if verbose:
        #    print logbook.stream

    # para printar o que tem dentro do logbook;
    # for record in logbook:
    #     print(record)

    return population, logbook

def varAnd(population, toolbox, cxpb, mutpb):
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
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring

    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

#Individuo and #Operator genetic
IND_SIZE = 104
# POPULACAO = int(sys.argv[2])
# CROSSOVER=float(sys.argv[4])
# GERACOES=int(sys.argv[3])
# TAXA_MUTACAO = float(sys.argv[6])
# TORNEIO=int(sys.argv[5])
# HALL_OF_FAME = 10
# ELITISMO = int(sys.argv[7])

POPULACAO = 500
TORNEIO = 2
CROSSOVER = 0.7
TAXA_MUTACAO = 0.01
GERACOES = 100
HALL_OF_FAME = 10
ELITISMO = 1

# Function Max


# O creator cria uma nova classe com o nome passado no parâmetro
# Em termos mais simples, essa linha de código cria uma nova classe de aptidão chamada FitnessMulti que tem dois componentes. 
# O primeiro componente é positivo e o segundo componente é negativo. A biblioteca Deap irá minimizar o segundo componente 
# da aptidão, o que significa maximizar o primeiro componente da aptidão.
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))

# array.array -> é usado para criar um arranjo de tipos específicos.
# no caso o Type code é i, logo ele cria um arranjo de inteiros
# Ele cria um arranjo com os elementos do fitnes.
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMulti)

# Attribute generator
toolbox = base.Toolbox()

# O método register registra uma função na biblioteca Deap com o nome passado e você pode fornecer argumentos padrão que serão passados ​​automaticamente 
# ao chamar a função registrada. Argumentos fixos podem então ser substituídos no momento da chamada da função.

# Em específico essa função gera uma função que quando chamada ela gera números aleatórios entre 1 e 0;
toolbox.register("indices", random.randint, 0, 1)

# A função tools.initRepeat repete um procedimento uma quantidade específica de vezes, no caso abaixo
# seria a quantidade de vezes do IND_SIZE.
# Essa função registra um indivíduo e inicializa ele com 0s - 1s aleatórios e repete IND_SIZE vezes.
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, IND_SIZE)

# Essa função registra uma função de colocar indivíduos em uma lista e repete toolbox.individual vezes 
# (quantidade de indivíduos).
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operadores genetic
# registra uma função de seleção de indivíduo do NSGA2 
toolbox.register("select", tools.selNSGA2)

# registra uma função que executa um cruzamento de dois pontos nos indivíduos da sequência de entrada
toolbox.register("mate", tools.cxTwoPoint)

# registra uma função que embaralhe os atributos do indivíduo de entrada e retorne o mutante. 
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=TAXA_MUTACAO)

# registra a função criada evaluate na biblioteca Deap
toolbox.register("evaluate", evaluate)

# faz o cruzemento entre pais, gera os filhos e armazena pai e filho juntos
toolbox.decorate("mate", mate_decorator)

hof = tools.HallOfFame(HALL_OF_FAME)
#toolbox.register("map", dtm.map)

def main():

    print("passei aqui")

    a = datetime.datetime.now()

    # gera uma semente aleatória
    # random.seed(sys.argv[1])
    random.seed(1)

    CarregaProteinas(PATH_BASE)
    CarregaProteinasExternas(PATH_BASE_EXTERNA)

    # inicializa uma lista com os indivíduos da população
    pop = toolbox.population(n=POPULACAO)
    # print(pop)
    # print(type(pop))

    for p in pop:
        # Inicializa uma lista vazia para os pais dos indivíduos. 
        p.pais = []
        # print(p.pais)


    for p in pop:
        # percorre cada indivíduo
        # print(p,"\n")
        for i in range(0, IND_SIZE):
            # print(i,"\n")
            # Se o índice atual estiver entre os valores especificados no passo anterior, ele define 
            # o valor no índice i do indivíduo p como 1.
            if(i == 0 or i == 1 or i == 50 or i == 51 or i == 52 or i == 103):
                p[i] = 1
            else:
                p[i] = 0

    stats1 = tools.Statistics(lambda ind: ind.fitness.values)


    # na biblioteca 

    stats1.register("1) Media   ", numpy.mean,axis=0)
    # numpy.std calcula o desvio padrão.
    stats1.register("2) Desvio Padrao   ", numpy.std,axis=0)
    stats1.register("3) Minimo  ", numpy.min,axis=0)
    stats1.register("4) Maximo  ", numpy.max,axis=0)

    stats2 = tools.Statistics(lambda ind: ind)
    stats2.register("Piores / Melhores  ", contaFilhos)
    stats2.register("Ind. Repetidos	 ", contaIndividuosIguais)

    stats = tools.MultiStatistics(Fitness=stats1, Filhos=stats2)

    eaMulti(pop, toolbox, CROSSOVER, TAXA_MUTACAO, GERACOES, POPULACAO, stats=stats, halloffame=hof)
    
    # guarda os melhores e escreve no arquivo.
    MELHORES = open("melhores/" + sys.argv[1] + '.txt', "a+")
    MELHORES.write('\nHALL OF FAME:')
    for elem in hof:
        MELHORES.write(elem.__str__() + elem.fitness.values.__str__() + '\n')

    #print('\nHALL OF FAME:')
    #for elem in hof:
    #    print (elem, elem.fitness.values)

    #b = datetime.datetime.now()
    #c = b - a

    #print '\n\nInicio : ', a.strftime("%A, %d %b %Y %H:%M:%S")
    #print 'Termino: ', b.strftime("%A, %d %b %Y %H:%M:%S")
    #print 'Duracao: ', divmod(c.days * 86400 + c.seconds, 60)

if __name__ == "__main__":
    main()




