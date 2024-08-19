#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import GridSearch
from sklearn.model_selection import cross_val_score
import sys
# from Arquivo import Arquivo

class ClassificadorT:

    def __init__(self, path, nomeArquivo):
        self.path = path
        self.nomeArquivo = nomeArquivo

    #receber a variável arquivo
    def fitness(self, algoritmoML, arquivo):
        dataset, classe = arquivo.prepara_data_frame(arquivo.get_nome_classe_arquivo_teste())
        scores = cross_val_score(algoritmoML, dataset, classe, cv=10, scoring='f1_macro')
        return scores.mean()
