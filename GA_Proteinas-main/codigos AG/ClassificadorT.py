#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from Arquivo import Arquivo

class Classificador:
    def fitness(self, individuo, algoritmoML):
        df, classe = Arquivo.load_Atributos(individuo, self.nomeClass)
        scores = cross_val_score(algoritmoML, df, classe, cv=10, scoring='f1_macro')
        return scores.mean()
