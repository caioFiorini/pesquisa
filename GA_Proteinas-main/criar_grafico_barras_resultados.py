import matplotlib.pyplot as plt

# Lista dos atributos
atributos = ["1 Attribute"] + [f"{i + 2} Attributes" for i in range(16)]

# Precisão simulada para cada atributo (em valores percentuais)
precisao = [0.513, 0.536, 0.540, 0.566, 0.590, 0.590, 0.594, 0.592, 0.597, 0.592, 0.581, 0.622, 0.637, 0.686, 0.677, 0.678, 0.680]

# Criando o gráfico de barras para precisão
plt.figure(figsize=(10, 6))
plt.bar(atributos, precisao, color='skyblue')

# Rotacionando os rótulos do eixo X para melhor leitura
plt.xticks(rotation=90)

# Adicionando título e rótulos
plt.title('Attribute Precision')
plt.xlabel('Attributes')
plt.ylabel('F1 Score')

# Exibir o gráfico
plt.tight_layout()
plt.show()
