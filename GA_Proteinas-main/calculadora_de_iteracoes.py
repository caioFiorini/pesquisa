import numpy as np

BARRA_N = '\n'

saida = False
while(saida != True):    
    print("Bem vindo a Caluculadora de Experimentos")
    seed_str = input("Digite os valores para as Sementes: \n Pode seguir o exemplo: 12354 45879 5632 (Quantas voce desejar utilizar! :)\n")
    seed = seed_str.split(' ')
    population_str = input("Digite os valores para Populacao min, max e o iterador:\n Pode seguir o exemplo: 15 30 9\n")
    population = population_str.split(' ')
    geracoes_str = input("Digite os valores para as Geracoes min, max e o iterador:\n Pode seguir o exemplo: 15 30 9\n")
    geracoes = geracoes_str.split(' ')
    cross_Over_Factor_str = input("Digite o valor do CrossOverFactor min, max e o iterador: \n Pode seguir o exemplo: 0.6 0.9 0.2\n")
    cross_Over_Factor = cross_Over_Factor_str.split(' ')
    tournamentSize = input("Digite o valor do Torneio: (Somente 1 valor)\n")
    mutation_rate_str = input("Digite o valor da Mutacao min, max e o iterador:\n Pode seguit o exemplo 0.2 0.4 0.1\n")
    mutation_rate = mutation_rate_str.split(' ')
    elitismo = input("Digite o valor do Elitismo: (somente 1 valor)\n")
    
    population_min = population[0].strip()
    population_max = population[1].strip()
    population_ite = population[2].strip()
    generations_min = geracoes[0].strip()
    generation_max = geracoes[1].strip()
    generation_ite = geracoes[2].strip()
    crossover_min = cross_Over_Factor[0].strip()
    crossover_max = cross_Over_Factor[1].strip()
    crossover_ite = cross_Over_Factor[2].strip()
    mutation_min = mutation_rate[0].strip()
    mutation_max = mutation_rate[1].strip()
    mutation_ite = mutation_rate[2].strip()
    numero_experimento = 0

    for i in seed:
        for j in np.arange(int(population_min), int(population_max), int(population_ite)):
            for k in np.arange(int(generations_min), int(generation_max), int(generation_ite)):
                if j % 4 != 0:
                    continue
                for l in np.arange(float(crossover_min), float(crossover_max), float(crossover_ite)):
                    for m in np.arange(float(mutation_min), float(mutation_max), float(mutation_ite)):
                        numero_experimento = numero_experimento+1
    
    print(f"Numero experimentos = {numero_experimento}")
    resp = input("Deseja calcular novamente a quantidade de experimentos? s para (sim) n para (não)\n")
    if (resp == 'n' or resp == 'nao' or resp == 'não'):
        saida = True

with(open('numero_experimento.txt', 'w')) as file:
    file.write(numero_experimento.__str__())

with(open('teste.txt', 'r')) as file:
    line = file.readlines()

with(open('teste.txt', 'w')) as file:
    file.write(line[0])
    file.write(line[1])
    file.write(f"seed {seed_str}\n")
    file.write(f"Population {population_str}\n")
    file.write(f"Generations {geracoes_str}\n")
    file.write(f"CrossOverFactor {cross_Over_Factor_str}\n")
    file.write(f"TournamentSize {tournamentSize.__str__()}\n")
    file.write(f"MutationRate {mutation_rate_str}\n")
    file.write(f"ElitismFactor {elitismo.__str__()}\n")
    file.write(line[9])

print("Se o valor das execuções foi 0, provavelmente é porque o número das iterações\n da popupalação não é divisível por 4;")
print("Agradecemos por poupar tempo de processamento ;)")