#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import csv
import numpy as np
from os.path import dirname
from os.path import join
from Arquivo import Arquivo

class Classificador:
    # contrutor
    def __init__(self, path, nomeArquivo, nomeClass):
        self.path = path
        self.nomeArquivo = nomeArquivo   
        self.nomeClass = nomeClass  
    
    def fitness(self, individuo, algoritmoML):
        df, classe = Arquivo.load_Atributos(individuo, self.nomeClass)
        scores = cross_val_score(algoritmoML, df, classe, cv=10, scoring='f1_macro')
        return scores.mean()
