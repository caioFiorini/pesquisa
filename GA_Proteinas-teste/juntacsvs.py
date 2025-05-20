import pandas as pd

# Carregar os arquivos CSV
base_treino = pd.read_csv('Base Treino Hipertensão.csv')
base_teste = pd.read_csv('Base Teste Hipertensão.csv')

# Juntar as duas bases
base_hipertensao = pd.concat([base_treino, base_teste], ignore_index=True)

# Salvar a nova base com o nome solicitado
base_hipertensao.to_csv('Base Hipertensão.csv', index=False)

