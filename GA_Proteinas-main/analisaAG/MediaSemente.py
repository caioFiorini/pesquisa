import os
import re
import matplotlib.pyplot as plt

path = "./melhores"
path_Media_geral = "./media_das_medias"

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

i = 0

for arquivo in arquivos:
    with open(os.path.join(path_Media_geral, arquivo), 'a') as file:
        file.write(str(media[i]))
    i += 1
