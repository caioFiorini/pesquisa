#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import GridSearch
from sklearn.model_selection import cross_val_score
import sys
sys.path.insert(0, '../Arquivo')
import Arquivo

class ClassificadorT:

    def __init__(self, path, nomeArquivo):
        self.path = path
        self.nomeArquivo = nomeArquivo


    def fitness(algoritmoML, atributo_ind):
        dataset, classe = Arquivo.dataframe_to_csv_test(atributo_ind)
        scores = cross_val_score(algoritmoML, dataset, classe, cv=10, scoring='f1_macro')
        return scores.mean()
