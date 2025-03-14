import os
import re

def processar_arquivos(diretorio_raiz):
    individuos = []
    colunas = [0] * 17  # Lista para armazenar as contagens de col_0 a col_16

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
    colunas_com_contagem = [(f"Coluna {idx}", count) for idx, count in enumerate(colunas)]

    # Ordena a lista de tuplas com base na contagem (ordem decrescente)
    colunas_ordenadas = sorted(colunas_com_contagem, key=lambda x: x[1], reverse=True)

    # Imprime as colunas e suas quantidades de 1's, ordenadas
    print("\nContagens ordenadas das colunas (decrescente):")
    for coluna, count in colunas_ordenadas:
        print(f"{coluna}: {count}")

# Exemplo de uso
processar_arquivos('resultados_teste/')
