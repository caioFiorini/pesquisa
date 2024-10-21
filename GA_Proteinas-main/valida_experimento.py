import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
import sys
import numpy as np
from sklearn.metrics import make_scorer, accuracy_score, f1_score, recall_score, precision_score, confusion_matrix, classification_report
from sklearn.base import clone
from sklearn.model_selection import KFold
import pickle
import os

# Função para realizar cross-validation e avaliar o modelo
def evaluate_model_with_cross_validation(model, X_rus, y_rus, cv=10, scoring='accuracy'):    
        melhor = 0
        labels = ['1', '2']  # respostas
        modelos = []
        
        # Definir os scorers
        scorers = {
            'accuracy': make_scorer(accuracy_score),
            'f1_score': make_scorer(f1_score, average='weighted', zero_division=1),  # zero_division=1 para F1-score
            'recall': make_scorer(recall_score, average='weighted', zero_division=1),  # zero_division=1 para Recall
            'precision': make_scorer(precision_score, average='weighted', zero_division=1)  # zero_division=1 para Precisão
        }
        
        # Preparar validação cruzada
        kf = KFold(n_splits=cv)
        
        # Inicializar listas para armazenar os resultados
        results = []
        
        # Realizar a validação cruzada
        for fold, (train_index, test_index) in enumerate(kf.split(X_rus, y_rus), 1):
            X_train, X_test = X_rus.iloc[train_index], X_rus.iloc[test_index]
            y_train, y_test = y_rus.iloc[train_index], y_rus.iloc[test_index]
            
            # Clonar o modelo para evitar o ajuste acumulativo
            cloned_model = clone(model)
            
            # Treinar o modelo
            cloned_model.fit(X_train, y_train)

            # Armazenar os modelos
            modelos.append(cloned_model)
            # Calcular as métricas no conjunto de treino
            y_pred_train = cloned_model.predict(X_train)
            
            # Calcular as métricas no conjunto de treino
            accuracy = accuracy_score(y_train, y_pred_train)
            f1 = f1_score(y_train, y_pred_train, average='weighted', zero_division=1)
            recall = recall_score(y_train, y_pred_train, average='weighted', zero_division=1)
            precision = precision_score(y_train, y_pred_train, average='weighted', zero_division=1)
            
            # Armazenar a matriz de confusão e o relatório de classificação
            cm = confusion_matrix(y_train, y_pred_train)
            cr = classification_report(y_train, y_pred_train, target_names=labels)
            
            # Armazenar os resultados formatados
            fold_result = {
                'fold': fold,
                'accuracy': accuracy,
                'f1_score': f1,
                'recall': recall,
                'precision': precision,
                'confusion_matrix': cm,
                'classification_report': cr
            }
            
            results.append(fold_result)
        
        f1_scores = [result['f1_score'] for result in results]

        aux = 0
        id_melhor_modelo = 0

        for i, j in enumerate(f1_scores):
            if aux < j:
                aux = j
                id_melhor_modelo = i
        
        best_model = modelos[id_melhor_modelo]
        best_score = aux        
        return best_score, best_model

# Função para salvar o melhor modelo
def selec_best_model(model):
    # Verificar se o arquivo existe
    with open('modelo_treinado.pkl', 'wb') as file:
        pickle.dump(model, file)

# Carregar o dataset
dataset = pd.read_csv("AVCBalanceado-AG.csv")

# Separar os dados de entrada e saída
dataset_classe = dataset["AVC"]
dataset_sem_classe = dataset[["Gênero", "Categoria_Alcool_Semanal", "Diabetes", "Categoria_AtividadeI", 
                             "classificacao_alimentacao", "Categoria_Fumantes", "Doenças Mentais", 
                             "Trabalho Doméstico Pesado", "Categoria_AtividadeM", "Consumo_Sal", 
                             "Colesterol_Alto", "Depressão", "Doença_Cardíaca", "Hipertensão"]]

# Definir o modelo de machine learning
algoritmoML = DecisionTreeClassifier(max_depth=5)

# Avaliar o modelo com validação cruzada
scores, best_model = evaluate_model_with_cross_validation(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')

# Selecionar o melhor modelo e salvar
selec_best_model(best_model)

# Exibir o F1-score
print(f"F1_score: {scores}")
