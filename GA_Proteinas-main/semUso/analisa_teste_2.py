import os
import re
import pandas as pd

def processar_arquivos(diretorio_raiz):
    individuos = []
    nomes = []
    colunas = [0] * 46  # Lista para armazenar as contagens de col_0 a col_16

    df = pd.read_csv("BaseColesterol_posprocessFinal.csv")

    for root, dirs, files in os.walk(diretorio_raiz):
        for file in files:
            if file.endswith('.txt'):  # ou a extensão que seus arquivos usam
                caminho_arquivo = os.path.join(root, file)
                with open(caminho_arquivo, 'r') as f:
                    for indice_linha, linha in enumerate(f, start=1):
                        # Extrair os valores entre colchetes usando expressão regular
                        match = re.search(r'\[(.*?)\]', linha)
                        if match:
                            individuo = list(map(int, match.group(1).split(',')))
                            individuos.append(individuo)

    # Atualiza a contagem de 1's em cada coluna
    for i in individuos:
        for j, k in enumerate(i):
            if k == 1:
                colunas[j] += 1

    # Cria uma lista de tuplas (coluna, quantidade de 1's)
    colunas_com_contagem = [(df.columns[idx+1].__str__(), count) for idx, count in enumerate(colunas)]

    # Ordena a lista de tuplas com base na contagem (ordem decrescente)
    colunas_ordenadas = sorted(colunas_com_contagem, key=lambda x: x[1], reverse=True)
    
    for i in colunas_ordenadas:
        print(i)
    j=0
    # Imprime as colunas e suas quantidades de 1's, ordenadas
    print("\nOrdem de aparições dos atributos:")
    for coluna, count in colunas_ordenadas:
        nomes.append(coluna)
        print(f"{j}, {coluna}: {count}")
        j= j+1
        
    print(nomes)

processar_arquivos('outputs/Experimentos/')