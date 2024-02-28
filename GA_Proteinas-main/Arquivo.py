import pandas as pd
import os

class Arquivo:
    def arquivo(self, nomeArquivo):
        if '.csv' not in nomeArquivo:
            print('Por favor envie um arquivo do tipo csv')
        
        localArquivo = os.path.join(nomeArquivo)
        self.dataset = pd.read_csv(localArquivo)

    def dataSet(self):
        return self.dataset


    def classes(self):
        classes = self.dataset.columns    
        return classes

#teste
algo = Arquivo()
algo.arquivo('Iris.csv')