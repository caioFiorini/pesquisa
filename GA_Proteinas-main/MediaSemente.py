import os
import re
import matplotlib.pyplot as plt

path = "./melhores"

arquivos = os.listdir(path)
lista = []
i = 0
soma = 0
media = []

for arquivo in arquivos:
    with open(os.path.join(path, arquivo), 'r') as file:
        for linha in file:
            linha = linha.replace("\n", " ")
            p = re.compile(r"(\d+\.\d+)\,")
            aux = p.findall(linha)
            if aux != []:
                lista.append(aux.__getitem__(0))

while i != lista.__len__():
    soma += float(lista[i])
    i += 1
    if i>0 and i%11 == 0:
         # cada posição da lista é 1 semente;
        media.append(soma/11)
        soma = 0

# Criar o gráfico de linha
plt.figure(figsize=(6, 6))  # Tamanho da figura (opcional)

plt.plot(arquivos, media, marker='o', linestyle='-', color='b', label='Média')

# Definir rótulos e título
plt.xlabel('Sementes')
plt.ylabel('Média Sementes')
plt.title('Média de cada semente')
plt.grid(True)

# Adicionar rótulos aos pontos
for i, rate in enumerate(media):
    plt.text(arquivos[i], rate, f'{rate:.2f}', ha='center', va='bottom')

# Adicionar legenda
plt.legend()

# Exibir o gráfico
plt.show()
