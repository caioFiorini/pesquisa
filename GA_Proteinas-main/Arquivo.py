import pandas as pd
import os

class Arquivo:
    def arquivo(self, nomeArquivo):
        if '.csv' not in nomeArquivo:
            print('Por favor envie um arquivo do tipo csv')
        
        localArquivo = os.path.join(nomeArquivo)
        self.dataset = pd.read_csv(localArquivo)
        self.classes = self.dataset.columns
        return self.dataset

    

#teste
arquivo = Arquivo()

algo = arquivo.arquivo('Iris.csv')