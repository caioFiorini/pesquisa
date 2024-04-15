#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy


class FileManager:
    def __init__(self, numeroAmostras, listaClasses, tamanhoTransformada):
        self.numeroAmostras = numeroAmostras
        self.listaClasses = listaClasses
        self.tamanhoTransformada = tamanhoTransformada
        self.arquivo = ""

    @staticmethod
    # modificar essa função
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
            + ",Hidrolases,Isomerases,Liases,Ligases,Oxidoredutases,Transferases\n" #retirar essa linha
        )
        self.CorpoArquivoCSV(
            path_Base,
            arquivoSaida,
            listaCaracteristica,
        )

    def CorpoArquivoCSV(
        self,
        path_Base,
        arquivoSaida,
        listaCaracteristica,
        listaCaracteristicaExternas,
        MATRIZ_PROTEINAS,
        MATRIZ_PROTEINAS_EXTERNAS,
    ):
        matrizExternas = MATRIZ_PROTEINAS_EXTERNAS[0]

        for contador, list in enumerate(MATRIZ_PROTEINAS):
            matriz = matriz = numpy.array(list)

            for caracteristica in listaCaracteristica:
                for m in matriz:
                    str = m[caracteristica].replace(",", ".").__str__()
                    arquivoSaida.write(str + ",")

            for caracteristicaExterna in listaCaracteristicaExternas:
                strExt = (
                    matrizExternas[contador][caracteristicaExterna]
                    .replace(",", ".")
                    .__str__()
                )
                arquivoSaida.write(strExt + ",")

            numeroclasse = 0
            if contador < 162:
                numeroclasse = 0
            elif contador < 217:
                numeroclasse = 1
            elif contador < 279:
                numeroclasse = 2
            elif contador < 295:
                numeroclasse = 3
            elif contador < 372:
                numeroclasse = 4
            elif contador >= 372:
                numeroclasse = 5

            str = numeroclasse.__str__() + "\n"
            arquivoSaida.write(str)

    def openDados(self, path, classe, extensao):
        caminho = os.path.join(path + "/" + classe + "/" + classe + extensao)
        arq = open(caminho, "r")
        return arq
