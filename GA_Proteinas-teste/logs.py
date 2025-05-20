import os
class Logs:
    def extrair_filhos_repetidos_por_geracao(diretorio_logs):
        resultado_por_geracao = []  # Lista para armazenar os dados de cada geração

        # Percorrer os arquivos na pasta
        for root, dirs, files in os.walk(diretorio_logs):
            for file in files:
                # Verificar se o nome do arquivo contém 'output'
                if 'output' in file:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        linhas = f.readlines()
                        geracao_atual = None  # Variável para armazenar a geração atual
                        
                        # Percorrer as linhas do arquivo e extrair dados
                        for linha in linhas:
                            if "Numero da geracao" in linha:  # Encontrar a linha que contém a geração
                                geracao_atual = int(linha.split(":")[1].strip())  # Extrair o número da geração
                            
                            if "Total de filhos repetidos" in linha and geracao_atual is not None:
                                # Extrair o número de filhos repetidos
                                total_filhos_repetidos = int(linha.split(":")[1].strip())
                                
                                # Armazenar o valor em uma lista de tuplas
                                resultado_por_geracao.append((geracao_atual, total_filhos_repetidos))
                                geracao_atual = None  # Resetar a geração atual para evitar reutilização incorreta
        
        return resultado_por_geracao
