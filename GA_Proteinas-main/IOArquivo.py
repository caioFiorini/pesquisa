#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os
import numpy
import copy

class LeituraArquivo:

    def __init__(self, numeroAmostras, listaClasses, tamanhoTransformada):
        self.numeroAmostras = numeroAmostras
        self.listaClasses = listaClasses
        self.tamanhoTransformada = tamanhoTransformada
        self.arquivo = ""

    def openTxt(self, path_Base, classe):
        caminho = os.path.join(path_Base, classe, classe + ".txt")
        arq = open(caminho, 'r')
        return arq


    def BuildCSV(self, path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS):
        features = (listaCaracteristica.__len__() * self.tamanhoTransformada + listaCaracteristicaExternas.__len__()).__str__()
        arquivoSaida.write(
            self.numeroAmostras.__str__() + "," + features + ",Hidrolases,Isomerases,Liases,Ligases,Oxidoredutases,Transferases\n");
        self.CorpoArquivoCSV(path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS)

    def CorpoArquivoCSV(self, path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas, MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS):
        matrizExternas = MATRIZ_PROTEINAS_EXTERNAS[0]

        for contador, list in enumerate(MATRIZ_PROTEINAS):
            matriz = matriz = numpy.array(list)

            for caracteristica in listaCaracteristica:
                for m in matriz:
                    str = m[caracteristica].replace(",", ".").__str__()
                    arquivoSaida.write(str + ",")

            for caracteristicaExterna in listaCaracteristicaExternas:
                strExt = matrizExternas[contador][caracteristicaExterna].replace(",", ".").__str__()
                arquivoSaida.write(strExt + ",")

            numeroclasse = 0
            if (contador < 162):
                numeroclasse = 0
            elif (contador < 217):
                numeroclasse = 1
            elif (contador < 279):
                numeroclasse = 2
            elif (contador < 295):
                numeroclasse = 3
            elif (contador < 372):
                numeroclasse = 4
            elif (contador >= 372):
                numeroclasse = 5

            str = numeroclasse.__str__() + "\n";
            arquivoSaida.write(str);


    def BuildCSV_WEKA(self, path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas, MATRIZ_PROTEINAS,
                 MATRIZ_PROTEINAS_EXTERNAS):
        features = (
        listaCaracteristica.__len__() * self.tamanhoTransformada + listaCaracteristicaExternas.__len__())

        contador = 0
        for x in xrange(features + 1):
            if(x == 0):
                contador = contador + 1
                arquivoSaida.write(contador.__str__())
            else:
                contador = contador + 1
                arquivoSaida.write("," + contador.__str__())

        arquivoSaida.write("\n")

        self.CorpoArquivoCSV_WEKA(path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas,
                             MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS)

    def CorpoArquivoCSV_WEKA(self, path_Base, arquivoSaida, listaCaracteristica, listaCaracteristicaExternas,
                        MATRIZ_PROTEINAS, MATRIZ_PROTEINAS_EXTERNAS):
        matrizExternas = MATRIZ_PROTEINAS_EXTERNAS[0]

        for contador, list in enumerate(MATRIZ_PROTEINAS):
            matriz = matriz = numpy.array(list)

            for caracteristica in listaCaracteristica:
                for m in matriz:
                    str = m[caracteristica].replace(",", ".").__str__()
                    arquivoSaida.write(str + ",")

            for caracteristicaExterna in listaCaracteristicaExternas:
                strExt = matrizExternas[contador][caracteristicaExterna].replace(",", ".").__str__()
                arquivoSaida.write(strExt + ",")

            numeroclasse = ""
            if (contador < 162):
                numeroclasse = "Hidrolases\n"
            elif (contador < 217):
                numeroclasse = "Isomerases\n"
            elif (contador < 279):
                numeroclasse = "Liases\n"
            elif (contador < 295):
                numeroclasse = "Ligases\n"
            elif (contador < 372):
                numeroclasse = "Oxidoredutases\n"
            elif (contador >= 372):
                numeroclasse = "Transferases\n"

            strValor = numeroclasse;
            arquivoSaida.write(strValor);

    def openDados(self, path, classe, extensao):
        caminho = os.path.join(path + "/" + classe + "/" + classe + extensao)
        arq = open(caminho, 'r')
        return arq


