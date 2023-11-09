import os
import matplotlib.pyplot as plt

path = "./media_das_medias"


arquivos = os.listdir(path)

lista = []
i = 0
soma = 0

for arquivo in arquivos:
    with open(os.path.join(path, arquivo), 'r') as file:
        lista.append(file.read())

while i != lista.__len__():
    soma += float(lista[i])
    i += 1

media = soma/lista.__len__()

# Criar o gráfico de linha
plt.figure(figsize=(6, 6))  # Tamanho da figura (opcional)

plt.plot(media, marker='o', linestyle='-', color='b', label='Média')

# Definir rótulos e título
plt.xlabel('Sementes')
plt.ylabel('')
plt.title('Média Experimento')
plt.grid(True)

# Adicionar legenda
plt.legend()

# Exibir o gráfico
plt.show()
plt.savefig('mediaSementes.png')