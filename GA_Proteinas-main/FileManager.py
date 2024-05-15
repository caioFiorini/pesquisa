#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy
from Arquivo import Arquivo

class FileManager:
    def __init__(self, numeroAmostras, tamanhoTransformada):
        self.numeroAmostras = str(numeroAmostras)
        # self.listaClasses = listaClasses
        self.tamanhoTransformada = tamanhoTransformada
        self.arquivo = ""

    @staticmethod
    # modificar essa função
    # abre o arquivo
    def get_text_file_contents(base_path: str, protein_class: str): # <----------
        file_path = os.path.join(base_path, protein_class, protein_class + ".txt")# <------
        text_file = open(file_path, "r")
        return text_file

    def BuildCSV(
        self,
        arquivoSaida,
        listaCaracteristica,
        arquivo
    ):
        features = (listaCaracteristica.__len__() * self.tamanhoTransformada).__str__()
        print(features)
        # arquivoSaida.write(
        #     "".join(self.numeroAmostras)
        #     + ","
        #     + features
        #     + ","+arquivo.retorna_nome_atributos()
        # )
        for i in listaCaracteristica:
            print(i)
        arquivoSaida.write("{},{},{}".format(self.numeroAmostras, features, arquivo.retorna_nome_atributos())) 
        arquivo = open(arquivoSaida.name, 'w')
        arquivo.write(features)
        arquivo.write(str(listaCaracteristica))
        arquivo.close
        
    def openDados(self, path, classe, extensao):
        caminho = os.path.join(path + "/" + classe + "/" + classe + extensao)
        arq = open(caminho, "r")
        return arq
