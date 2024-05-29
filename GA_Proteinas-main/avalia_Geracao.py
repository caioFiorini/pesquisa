# ideia do algoritmo
# ler os arquivos melhores 
# armazenar em alguma estrutura de dados
# calcular a média dos experimentos e guardar em um vetor
# comparar todos os experimentos
# printar o que for melhor
import pandas as pd
import sys 
import os

DIRETORIO = "/outputs/Experimentos/experiment_"
quantidade_experimentos = int(sys.argv[1])

def encontrar_arquivo(pasta, nome_arquivo):
    print(pasta)
    caminho = None
    # Percorre todos os arquivos na pasta
    for root, files in os.walk(pasta):
        print("passei aqui"+str(files))
        for file in files:
            print(file)
            # Verifica se o nome do arquivo corresponde ao nome procurado
            if file.startswith(nome_arquivo):
                caminho = os.path.join(root, file)  # Retorna o caminho completo do arquivo
    # Retorna None se o arquivo não for encontrado
    return caminho

def main():

    for i in range(1, quantidade_experimentos+1):
        diretorio = DIRETORIO+str(i)+'/'
        caminho = encontrar_arquivo(diretorio, "Melhores_")
        print(caminho)


if __name__ == "__main__":
    main()