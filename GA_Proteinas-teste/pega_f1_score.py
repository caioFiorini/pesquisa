import os

DIRETORIO = './Resultado_experimentos'

def encontrar_arquivos(diretorio, padrao):
    arquivos_encontrados = []
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.startswith(padrao):
                arquivos_encontrados.append(os.path.join(root, file))
    return arquivos_encontrados

def calcular_estatisticas(valores):
    maior_valor = max(valores)
    menor_valor = min(valores)
    valor_medio = sum(valores) / len(valores)
    return maior_valor, menor_valor, valor_medio

def retorna_dados():
    resultados = []

    # Alterando o diretório base para Resultado_experimentos
    base_diretorio = 'Resultado_experimentos/'

    experimentos = encontrar_arquivos(base_diretorio, "Melhores_")
    for k in experimentos:
        with open(k, "r") as file:
            # Pegando apenas a primeira linha do arquivo
            line = file.readline()
            split_result = line.split('(')
            linha_dado = split_result[2]
            split_result = linha_dado.split(',')
            erro = float(split_result[0])
            resultados.append(erro)

    # Calcular as estatísticas
    maior_valor, menor_valor, valor_medio = calcular_estatisticas(resultados)

    return resultados, maior_valor, menor_valor, valor_medio

# Certifique-se de definir a variável DIRETORIO antes de chamar a função main


