import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score, recall_score, precision_score, make_scorer
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_score
from sklearn import tree
import matplotlib.pyplot as plt
import pickle

class Validacao:
    # recebe um objeto do tipo dataset, com o dataset aberto, puxa do arquivo
    def valida_sem_salvar_modelo(self, dataset, nome_classe, colums_list):
        dataset_ = dataset
        dataset_.columns = dataset_.columns.str.strip()
        score = []
        print(nome_classe)
        min_count = dataset_[nome_classe].value_counts().min()
        dataset_ = dataset_.groupby(nome_classe).sample(n=min_count, random_state=4)
        # a princípio vou utilizar as colunas conforme o algoritmo genético soltar
        dataset_classe = dataset_[nome_classe]
        dataset_ = dataset_.drop(columns = [nome_classe])
        colunas_iniciais  = colums_list
        
        for i in range(1, len(colunas_iniciais)):
            colunas_atualizadas = colunas_iniciais[:i]  # Seleciona as primeiras i colunas
            
            dataset_sem_classe = dataset_.iloc[:, :i] # Seleciona o dataset_ com as colunas atualizadas
            
            # Definir o modelo de machine learning
            algoritmoML = DecisionTreeClassifier(max_depth=5)
            
            # Avaliar o modelo com validação cruzada
            # scores, best_model = evaluate_model_with_cross_validation(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')
            scores = cross_val_score(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring="f1_macro")
            score.append(scores.mean())
            # Exibir o F1-score e a quantidade de colunas utilizadas na iteração atual
            print(f"Quantidade de atributos: {len(colunas_atualizadas)}, F1_score: {scores.mean()}")
