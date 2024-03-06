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
    
    
    
    
    
    def load_Arquivo_Nome_Nao_Passa_Por_Parametro(self):
        return 0

    def load_Arquivo_Nome_Passado_Por_Parametro(self, nomeClass):
        
        dataset = pd.read_csv('Iris.csv')
        
        
        # A ideia é que o usuário informe o nome da classe ou simplesmente pegamos a última.
        
        # teste        
        respostas = dataset[nomeClass]
        print(respostas)
        
        dataset = dataset.drop(nomeClass, axis=1)
        print(dat)
        
        # Código que tinha antes
        
        # temp = next(data_file)
        # n_samples = int(temp[0]) #amostras
        # n_features = int(temp[1])  #características
        # target_names = np.array(temp[2:])
        # data = np.empty((n_samples, n_features))
        # target = np.empty((n_samples,), dtype=np.int64)

        # for i, ir in enumerate(data_file):
        #     data[i] = np.asarray(ir[:-1], dtype=np.float64)
        #     target[i] = np.asarray(ir[-1], dtype=np.int64)
                
#teste
algo = Arquivo()
algo.arquivo('Iris.csv')

arquivo = algo.load_Arquivo_Nome_Passado_Por_Parametro("class")
