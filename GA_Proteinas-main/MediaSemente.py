import os
import re

path = "./melhores"

arquivos = os.listdir(path)
lista = []

for arquivo in arquivos:
    with open(os.path.join(path, arquivo), 'r') as file:
        conteudo = file.read()
        lista.append(conteudo)
        

for i in lista:
    aux = i
    lista2 = aux.split("(")
    
print(lista2)