import matplotlib.pyplot as plt

# Lista dos atributos
atributos = ['Gênero', 'Freq.Etnia', 'Consumo Sal', 'Trabalho Doméstico Pesado', 'Hipertensão',
             'Diabetes', 'Colesterol Alto', 'Doença Cardíaca', 'Depressão', 'Doenças Mentais', 
             'Categoria IMC', 'Jornada de Trabalho', 'Categoria Fumantes', 'Categoria Alcool Semanal',
             'classificacao alimentacao', 'Categoria AtividadeI', 'Categoria AtividadeM']

# Frequência simulada para cada atributo   
frequencias = [248, 118, 162, 174, 133, 217, 157, 135, 155, 178, 119, 132, 188, 239, 193, 214, 170]

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(atributos, frequencias, color='skyblue')

# Rotacionando os rótulos do eixo X para melhor leitura
plt.xticks(rotation=90)

# Adicionando título e rótulos
plt.title('Frequency of Attributes Facing Individuals')
plt.xlabel('Attributes')
plt.ylabel('Frequency')

# Exibir o gráfico
plt.tight_layout()
plt.show()
