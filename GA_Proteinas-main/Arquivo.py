import pandas as pd

class arquivo:
    def arquivo(self, nomeArquivo):
        if '.csv' not in nomeArquivo:
            print('Por favor envie um arquivo do tipo csv')
        
        self.dataset = pd.read_csv(nomeArquivo)
        self.classes = self.dataset.columns
        return self.dataset

    

#teste
# novoArquivo = arquivo('Iris.csv')