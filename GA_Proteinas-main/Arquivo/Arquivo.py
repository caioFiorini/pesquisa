import pandas as pd
import os
import os.path as dirname
import os.path as join
import numpy as np
import csv

class Arquivo:
    def arquivo(self, nomeArquivo):
        if '.csv' not in nomeArquivo:
            print('Por favor envie um arquivo do tipo csv')
        
        self.localArquivo = os.path.join(nomeArquivo)
        self.dataset = pd.read_csv(self.localArquivo)

    def dataSet(self):
        return self.dataset


    def classes(self):
        classes = self.dataset.columns    
        return classes
    
    def dataframe_to_csv_test(self, nomeClass = "n"):
        dataset = pd.read_csv('Iris.csv')

        # A ideia é que o usuário informe o nome da classe ou simplesmente pegamos a última.
        if(nomeClass != "n"):
            # teste (funciona)     
            respostas = dataset[nomeClass]
            print(respostas)
            
            dataset = dataset.drop(nomeClass, axis=1)
            print(dataset)
        
        #pego a última coluna e removo ela!
        nome_ultima_coluna = dataset.columns[dataset.columns.__len__()-1]
        ultima_coluna = dataset[nome_ultima_coluna]
        dataset = dataset.drop(nome_ultima_coluna, axis=1)
        
        #  classe = dataset[nomeClass]
        # # print(classe)
        # dataset = dataset.drop(nomeClass, axis=1)
        # # print(dataset)
        # return dataset, classe
    
#teste
algo = Arquivo()
algo.arquivo('Iris.csv')

# arquivo = algo.load_Arquivo_Nome_Passado_Por_Parametro("class")

arquivo = algo.load_Arquivo_Nome_Passado_Por_Parametro()
