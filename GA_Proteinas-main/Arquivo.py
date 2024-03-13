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
    
    #melhorar o nome dessa função depois.
    #adicionar o indivíduo como parâmetro.
    # O nome da classe é algo extremamente importante
    
    def load_Atributos(self, individuo, nomeClass):
        
        dataset = self.dataset
        individuo = [0,1,0,1]
        for i,ind in enumerate(individuo):
            # print(i)
            # print("Individuo: " + str(ind))
            if(ind == 0):
                dataset = dataset.drop(dataset.columns[i],axis=1)
                
        classe = dataset[nomeClass]
        # print(classe)
        dataset = dataset.drop(nomeClass, axis=1)
        # print(dataset)
        return dataset, classe
    
#teste
algo = Arquivo()
algo.arquivo('Iris.csv')

arquivo = algo.load_Atributos("class")