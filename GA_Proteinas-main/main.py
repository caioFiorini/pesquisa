# Standard Library Imports
import array
import csv
import os
import random
import numpy as np
import time
import sys

# Third-party Library Imports
import numpy
from deap import base, creator, tools

# Local Imports
from MultiObjectiveGeneticAlgorithm import MultiObjectiveGeneticAlgorithm
from MOGAToolbox import MOGAToolbox as mt
from Arquivo import Arquivo
from algoritmo_Genetico import Algoritmo_Genetico
from algoritmos_ML import AlgoritmosML
from diretorio import Diretorio
from rankeamento import Rankeamento
from valida import valida_experimento

# ====== MARK: Defining paths and file names ======
CLASSIFIER_PATH = os.path.abspath("Individuos")
DIRETORIO_PATH = os.path.abspath(".outputs")
EXPERIMENTO_PATH = os.path.abspath("./Experimentos")
EXPERIMENTO_PATH_ = os.path.abspath("./Experimentos")
RESULTADOS_PATH = os.path.abspath("./Resultados_teste")


HALL_OF_FAME_SIZE = 10

def main():
    start_time = time.time()
    contador = 0
    diretorio = Diretorio(DIRETORIO_PATH)
    diretorio.create_folder(EXPERIMENTO_PATH)

    # parte do sistema de backup.
    

    
    
    
    # Leitura dos arquivos
    arquivo = Arquivo()
    linhas_arquivo = arquivo.le_arquivo_teste()
    arquivo_csv = linhas_arquivo[0].strip("\n").split(' ')
    nome_arquivo_teste = arquivo_csv[0]
    nome_classe_arquivo_teste = arquivo_csv[1]
    arquivo.le_arquivo(nome_arquivo_teste)    
    arquivo.set_nome_classe_arquivo_teste(nome_classe_arquivo_teste)
    SAMPLE_COUNT = arquivo.quantidade_linhas_colunas(0)
    INDIVIDUAL_SIZE = arquivo.quantidade_linhas_colunas(1)
    INDIVIDUAL_SIZE = INDIVIDUAL_SIZE-1
    mt.setup_creator()
        
    # Preparando os elementos para entrar no teste
    backup = linhas_arquivo[1].strip("\n").split(" ")
    seed = linhas_arquivo[2].strip("\n").split(" ")
    seed.pop(0)
    Population = linhas_arquivo[3].strip("\n").split(" ")
    Generations = linhas_arquivo[4].strip("\n").split(" ")
    CrossOverFactor = linhas_arquivo[5].strip("\n").split(" ")
    TournamentSize = linhas_arquivo[6].strip("\n").split(" ")
    TournamentSize.pop(0)
    MutationRate = linhas_arquivo[7].strip("\n").split(" ")
    ElitismFactor = linhas_arquivo[8].strip("\n").split(" ")
    ElitismFactor.pop(0)
    algoritmo_Ml = linhas_arquivo[9].strip("\n").split(" ")
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
    nome_classificador = algoritmo_Ml[0]

    # pega o algoritmo de machine learning
    algoritmo_ml = AlgoritmosML(nome_classificador, algoritmo_Ml)
    modelo_ml = algoritmo_ml.get_model()
    hall_of_fame = tools.HallOfFame(HALL_OF_FAME_SIZE)
    numero_experimento = 0

    todos_fitness = []

    with open("numero_experimento.txt", 'r') as file:
        line = file.readline()
        line = int(line)

    if numero_experimento == line:
        for i in seed:
            for j in np.arange(int(population_min), int(population_max), int(population_ite)):
                for k in np.arange(int(generations_min), int(generation_max), int(generation_ite)):
                    if j % 4 != 0:
                        continue
                    for l in np.arange(float(crossover_min), float(crossover_max), float(crossover_ite)):
                        for m in np.arange(float(mutation_min), float(mutation_max), float(mutation_ite)):
                            numero_experimento = numero_experimento+1
        with open("numero_experimento.txt", 'w') as file:
            file.write(str(numero_experimento))
            
    # parte que decide se irá começar a partir do ponto de parada do BACKUP, ou se começa uma nova.
    if int(backup[0]) == 0:
        conteudo = Arquivo.le_arquivo_txt(backup[1])
        conteudo = conteudo.split("\n")
        i = conteudo[0].split(":")
        i = float(i[1])
        j = conteudo[1].split(":")
        j = float(j[1])
        k = conteudo[2].split(":")
        k = float(k[1])
        l = conteudo[3].split(":")
        l = float(l[1])
        m = conteudo[4].split(":")
        m = float(m[1])
        contador = conteudo[5].split(":")
        contador = float(contador[1]) 
    else:
        contador = 0
    # For onde os testes irão acontecer, dentro dele acontecerá a criação das pastas e a escrita dos testes.
    for i in seed:
        CLASSIFIER_FILE_NAME = i + ".csv"
        for j in np.arange(int(population_min), int(population_max), int(population_ite)):
            if j % 4 != 0:
                continue
            for k in np.arange(int(generations_min), int(generation_max), int(generation_ite)):
                for l in np.arange(float(crossover_min), float(crossover_max), float(crossover_ite)):
                    for m in np.arange(float(mutation_min), float(mutation_max), float(mutation_ite)):
                        
                        # Ideia futura de Backup
                        parametros = f"i:{i}\nj:{j}\nk:{k}\nl:{l}\nm:{m}\ncontador:{contador}"
                        Arquivo.escreve_arquivo_backup(backup[1], parametros)
                            
                        l = round(l,3)
                        m = round(m,3)
                        random.seed(i)
                        path = "Experimento_"+ contador.__str__()
                        diretorio.create_folder_in_folder(path)
                        FILE_NAME = "seed_"+i.__str__()+"pop_"+j.__str__()+"gen_"+k.__str__()+"cross_"+l.__str__()+"muta_"+m.__str__() 
                        evolution_toolbox = mt(
                            INDIVIDUAL_SIZE,
                            m,
                            CLASSIFIER_FILE_NAME,
                            CLASSIFIER_PATH,
                            SAMPLE_COUNT,
                            TournamentSize[0],
                            arquivo,
                            modelo_ml,
                            FILE_NAME,
                            diretorio,
                            todos_fitness,
                            k
                        ).toolbox
                        # inicializa uma lista com os indivíduos da população
                        population = evolution_toolbox.population(n=j)
                        # Inicializa uma lista vazia para os pais dos indivíduos.
                        for individual in population:
                            individual.pais = []
                        
                        stats1 = tools.Statistics(lambda individual: individual.fitness.values)

                        stats1.register("1) Media   ", np.mean, axis=0)
                        stats1.register("2) Desvio Padrao   ", np.std, axis=0)
                        stats1.register("3) Minimo  ", np.min, axis=0)
                        stats1.register("4) Maximo  ", np.max, axis=0)

                        stats2 = tools.Statistics(lambda individual: individual)
                        stats2.register("Piores / Melhores  ", Algoritmo_Genetico.count_individuals_relative_to_parent_average)
                        stats2.register("Ind. Repetidos	 ", Algoritmo_Genetico.get_duplicate_individuals_count)

                        stats = tools.MultiStatistics(Fitness=stats1, Filhos=stats2)

                        print("Starting algorithm...")
                        multi_objective_genetic_algorithm = MultiObjectiveGeneticAlgorithm(
                            i,
                            population,
                            evolution_toolbox,
                            l,
                            m,
                            k,
                            j,
                            diretorio,
                            stats=stats,
                            hall_of_fame=hall_of_fame,
                            FILE_NAME=FILE_NAME
                        )

                        multi_objective_genetic_algorithm.execute()

                        # guarda os melhores e escreve no arquivo.
                        # print("\n\nSetting up hall of fame...")
                        melhores_path = "Melhores_" + FILE_NAME + ".txt"
                        diretorio_melhores = diretorio.constroi_caminho(diretorio.get_path(), melhores_path)
                        best_individuals = open(diretorio_melhores, "w")
                        # best_individuals.write("\nHALL OF FAME:")
                        for top_individual in hall_of_fame[1:]:
                            best_individuals.write(
                                top_individual.__str__() + top_individual.fitness.values.__str__() + "\n"
                            )
                        
                        # with open("todos_individuos.txt", "w") as file:
                        #     for i in todos_fitness:
                        #         file.write(i+"\n")

                        print("\nDone!")

                        duration = time.time() - start_time
                        hours, remainder = divmod(duration, 3600)
                        minutes, seconds = divmod(remainder, 60)

                        print(
                            f"Total execution time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds."
                        )
                        contador = contador + 1

    # # início do processo de rankeamento
    rank = Rankeamento()
    diretorio.remove_arquivos(RESULTADOS_PATH)
    rank.junta_arquivos(EXPERIMENTO_PATH_, RESULTADOS_PATH)
    colunas = rank.processa_arquivos_teste(EXPERIMENTO_PATH_, RESULTADOS_PATH, INDIVIDUAL_SIZE)
    colunas_para_filtrar = [item[0] for item in colunas]  
    # O -1 é para pegar o ultimo elemento do split, no caso vai ser o número da coluna
    colunas_tratadas = [int(coluna.split(" ")[-1].strip()) for coluna in colunas_para_filtrar]
    validacao = valida_experimento()
    dataset = arquivo.retorna_dataset()
    # print(dataset)
    validacao.valida_sem_salvar_modelo(dataset,nome_classe_arquivo_teste, colunas_tratadas)
    
    
if __name__ == "__main__":
    main()
