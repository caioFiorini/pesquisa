import matplotlib.pyplot as plt

# Lista dos atributos
atributos = ['Gênero', 'Freq.Etnia', 'Consumo_Sal', 'Trabalho Doméstico Pesado', 'Hipertensão',
             'Diabetes', 'Colesterol_Alto', 'Doença_Cardíaca', 'Depressão', 'Doenças Mentais', 
             'Categoria_IMC', 'Jornada de Trabalho', 'Categoria_Fumantes', 'Categoria_Alcool_Semanal',
             'classificacao_alimentacao', 'Categoria_AtividadeI', 'Categoria_AtividadeM']

# Frequência simulada para cada atributo
frequencias = [248, 118, 162, 174, 133, 217, 157, 135, 155, 178, 119, 132, 188, 239, 193, 214, 170]

# Ordenar os atributos e frequências da maior para a menor
atributos_ordenados, frequencias_ordenadas = zip(*sorted(zip(atributos, frequencias), key=lambda x: x[1], reverse=True))

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(atributos_ordenados, frequencias_ordenadas, color='skyblue')

# Rotacionando os rótulos do eixo X para melhor leitura
plt.xticks(rotation=90)

# Adicionando título e rótulos
plt.title('Frequência de Atributos Diante de Indivíduos (Ordenado)')
plt.xlabel('Atributos')
plt.ylabel('Frequência')

# Exibir o gráfico
plt.tight_layout()
plt.show()
