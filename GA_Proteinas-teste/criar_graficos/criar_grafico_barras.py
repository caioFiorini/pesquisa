import matplotlib.pyplot as plt

# Lista dos atributos
atributos = ['Gender', 'Ethnicity Frequency', 'Salt Consumption', 'Heavy Domestic Work', 'Hypertension',
 'Diabetes', 'High Cholesterol', 'Heart Disease', 'Depression', 'Mental Disorders', 
 'BMI Category', 'Work Hours', 'Smoking Category', 'Weekly Alcohol Category',
 'Food Classification', 'Light Activity Category', 'Moderate Activity Category']


# Frequência simulada para cada atributo   
frequencias = [248, 118, 162, 174, 133, 217, 157, 135, 155, 178, 119, 132, 188, 239, 193, 214, 170]

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(atributos, frequencias, color='skyblue')

# Rotacionando os rótulos do eixo X para melhor leitura
plt.xticks(rotation=90)

# Adicionando título e rótulos
plt.xlabel('Attributes')
plt.ylabel('Frequency')

# Exibir o gráfico
plt.tight_layout()
plt.show()
