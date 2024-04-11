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
    def fitness(algoritmoML):
        df, classe = Arquivo.dataframe_to_csv_test()
        scores = cross_val_score(algoritmoML, df, classe, cv=10, scoring='f1_macro')
        return scores.mean()
