import os
import re

path = "./melhores"

arquivos = os.listdir(path)
lista = []
i = 0
soma = 0

for arquivo in arquivos:
    with open(os.path.join(path, arquivo), 'r') as file:
        for linha in file:
            linha = linha.replace("\n", " ")
            p = re.compile(r"(\d+\.\d+)\,")
            aux = p.findall(linha)
            if aux != []:
                lista.append(aux.__getitem__(0))

while i != lista.__len__():
    if  i%11 != 0:
        soma += float(lista[i])
    else:
        media = soma/11
        soma = 0
        soma += float(lista[i])
    i += 1