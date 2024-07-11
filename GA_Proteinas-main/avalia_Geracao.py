# ideia do algoritmo
# ler os arquivos melhores 
# armazenar em alguma estrutura de dados
# calcular a média dos experimentos e guardar em um vetor
# comparar todos os experimentos
# printar o que for melhor
import pandas as pd
import sys 
import os
from Arquivo import Arquivo

DIRETORIO = "./outputs/Experimentos/experiment_"
quantidade_experimentos = int(sys.argv[1])

def main():
    media_experimentos = []
    experimentos_media = []
    experimento = []
    media = 0
    maior = 0
    melhor_experimento = 0
    iguais = 0
    contador = 0
    for i in range(1, quantidade_experimentos+1):
        diretorio = DIRETORIO+str(i)+'/'
        experimentos = Arquivo.encontrar_arquivo(diretorio, "Melhores_")
        for j in experimentos:
            # print(j)
            for k in j:        
                with open(k, "r") as file:
                    # print(k)
                    for line in file:
                        # print(line)
                        split_result = line.split('(')
                        linha_dado = split_result[2]
                        split_result = linha_dado.split(',')
                        erro = split_result[0]
                        media = media+float(erro)
                        contador = contador + 1
                    media = media/contador
                    contador = 0
                    experimentos_media.append(media)
                    media = 0
            media_experimentos.append(experimentos_media.copy())
            experimentos_media.clear()
        
    for i, j in enumerate(media_experimentos):
        # print(str(i) +'' + str(j)) 
        diretorio = DIRETORIO+str((i+1))+'/'
        with open(diretorio+"media_experimento"+str((i+1))+".txt", "w") as file:
            
            media = 0
            for k in j:
                media += k
            experimento.append(media)
            file.write(media.__str__())

    for i,j in enumerate(experimento):
        if j > maior:
            maior = j
            melhor_experimento = i+1
        elif j == maior:
            iguais = iguais + 1
       
    if iguais == experimento.__len__()-1:
        print("Os experimentos deram a mesma média.")
    else:
        print("Melhor experimento é o: " + str(melhor_experimento))
    
    # abrir melhor experimento.
    diretorio = DIRETORIO+str(melhor_experimento)+'/'
    with open(diretorio+"", "w") as file:
        
    # extrair o indivíduo
    # caso todos sejam iguais, abre o primeiro
    # encontrar arquivo()
    # fazer o undersampli da base de dados na classe arquivo
    # testar em um KNN
    # armazenar os dados da matriz
    # plotar a curva
    
    
    
if __name__ == "__main__":
    main()

    