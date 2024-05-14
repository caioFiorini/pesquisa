import pandas as pd
import os
import os.path as dirname
import os.path as join
import numpy as np
import sys
# Pega o diretório onde o arquivo Classificador está alocado.
sys.path.insert(0, '../codigos_AG')
from algoritmos_ML import AlgoritmosML

class Arquivo:

    def le_arquivo(self, nomeArquivo):
        if '.csv' not in nomeArquivo:
            print('Por favor envie um arquivo do tipo csv')
        
        self.localArquivo = os.path.join(nomeArquivo)
        self.dataset = pd.read_csv(self.localArquivo)
        # pega o nome dos atributos.
        self.atributos = self.dataset.columns.to_list()

    def retorna_nome_atributos(self):
        return self.atributos
    
    def quantidade_linhas_colunas(self, operador):
        
        if operador == 1:
            resposta = self.dataset.shape[1] # pega a quantidade de colunas
        elif operador == 0:
            resposta = self.dataset.shape[0] # pega a quantidade de linhas
        
        return resposta
    
    def arquivo_csv(self, numero_amostras, lista_classes, tamanho_transformada):
        self.numero_amostras = numero_amostras
        self.lista_classes = lista_classes
        self.tamanho_transformada = tamanho_transformada
        self.arquivo = ""
        
    def monta_csv(self, path_base, arquivo_saida, lista_caracteristicas):
        features = (lista_caracteristicas.__len__() * self.tamanho_transformada).__str__()
        arquivo_saida.write(
            self.numero_amostras.__str__()
            + ","
            + features
            + ","
            + Arquivo.retorna_nome_atributos()
        )
        self.corpo_arquivo_csv(path_base, arquivo_saida, lista_caracteristicas)
        
    def dataSet(self):
        return self.dataset


    def classes(self):
        classes = self.dataset.columns    
        return classes
    
    def prepara_data_frame(self, nomeClass = "class"):
        dataset = pd.read_csv('Iris.csv')

        # A ideia é que o usuário informe o nome da classe ou simplesmente pegamos a última coluna.
        if "class" not in nomeClass:
            #pego a última coluna e removo ela!
            nome_ultima_coluna = dataset.columns[dataset.columns.__len__()-1]
            classe = dataset[nome_ultima_coluna]
            dataset = dataset.drop(nome_ultima_coluna, axis=1)
            
            #  classe = dataset[nomeClass]
            # print(classe)
            # dataset = dataset.drop(nomeClass, axis=1)
            # print(dataset)

        classe = dataset[nomeClass]
        # print(classe)
            
        dataset = dataset.drop(nomeClass, axis=1)
        # dataset=dataset.drop(dataset.index[0])
        # print(dataset)
        return dataset, classe
    
    def retorna_quantidade_colunas(self):
        dataset, _ = self.prepara_data_frame()
        num_colunas = len(dataset.columns)
        return num_colunas
        
    
    def dataframe_to_csv_test(self, atributos_ind):
        
        dataset, classe = self.prepara_data_frame()
        
        # pega as colunas que tem 1
        cols_para_manter = [dataset.columns[i] for i in range(len(dataset.columns)) if atributos_ind[i] != 0]
        dataset = dataset[cols_para_manter]

        # print(df)
        return dataset, classe
            
# #teste
# algo = Arquivo()
# algo.arquivo('Iris.csv')

# # ml = Algoritmos_ML()

# atributo_individuo = [0,1,0,1,0]
# str = algo.prepara_data_frame(atributo_individuo)
