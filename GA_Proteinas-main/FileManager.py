#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy
from Arquivo import Arquivo


class FileManager:
    def __init__(self, numeroAmostras, listaClasses, tamanhoTransformada):
        self.numeroAmostras = numeroAmostras
        self.listaClasses = listaClasses
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
        path_Base,
        arquivoSaida,
        listaCaracteristica
    ):
        features = (listaCaracteristica.__len__() * self.tamanhoTransformada).__str__()
        arquivoSaida.write(
            self.numeroAmostras.__str__()
            + ","
            + features
            + ","+Arquivo.retorna_nome_atributos()
        )
        arquivo = open(arquivoSaida, 'w')
        arquivo.write(features)
        arquivo.write(listaCaracteristica)
        arquivo.close
        
        
        
        
    def openDados(self, path, classe, extensao):
        caminho = os.path.join(path + "/" + classe + "/" + classe + extensao)
        arq = open(caminho, "r")
        return arq
