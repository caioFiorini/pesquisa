#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import csv
import numpy as np
from os.path import dirname
from os.path import join

class Bunch(dict):
    """Container object for datasets

    Dictionary-like object that exposes its keys as attributes.

    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2
    >>> b.a = 3
    >>> b['a']
    3
    >>> b.c = 6
    >>> b['c']
    6

    """

    def __init__(self, **kwargs):
        super(Bunch, self).__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        pass

class Classificador:
    def __init__(self, path, nomeArquivo):
        self.path = path
        self.nomeArquivo = nomeArquivo

    def load_proteina(self, return_X_y=False):
        module_path = dirname(self.path)
        with open(join(module_path, self.nomeArquivo)) as csv_file:
            data_file = csv.reader(csv_file)
            temp = next(data_file)
            n_samples = int(temp[0])
            n_features = int(temp[1])
            target_names = np.array(temp[2:])
            data = np.empty((n_samples, n_features))
            target = np.empty((n_samples,), dtype=np.int)

            for i, ir in enumerate(data_file):
                data[i] = np.asarray(ir[:-1], dtype=np.float64)
                target[i] = np.asarray(ir[-1], dtype=np.int)

        if return_X_y:
            return data, target

        return Bunch(data=data, target=target,
                     target_names=target_names,
                     DESCR='Proteinas - Cada Classe representa uma determinada funcao',
                     feature_names=['Hidrolases', 'Isomerases', 'Liases', 'Ligases', 'Oxidoredutases', 'Transferases'])

    def fitness(self):
        arquivo = self.load_proteina()
        #parameters = {'kernel': ['rbf'], 'C': [1, 10, 100, 1000]}
        parameters = {'kernel': ['rbf'], 'C': [1000]}
        svr = svm.SVC()

        clf = GridSearchCV(svr, parameters, cv=10, scoring="accuracy")
        clf.fit(arquivo.data, arquivo.target)
        return clf.best_score_
        #return 45.01

    def fitness1(self):
        arquivo = self.load_proteina()

        clf = svm.SVC(kernel='rbf', C=1000)
        scores = cross_val_score(clf, arquivo.data, arquivo.target, cv=10, scoring='accuracy')
        #scores = cross_val_score(clf, arquivo.data, arquivo.target, cv=10, scoring='f1_macro')
        return scores.mean()
