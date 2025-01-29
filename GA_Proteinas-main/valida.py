import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score, recall_score, precision_score, make_scorer
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_score
from sklearn import tree
import matplotlib.pyplot as plt
import pickle

class valida_experimento:
    
    # Função para realizar cross-validation e avaliar o modelo
    # model = algoritmoML, X_rus = dataset_sem_classe, y_rus = dataset_classe, labels = respostas array
    def evaluate_model_with_cross_validation(model, X_rus, y_rus, respostas, cv=10, scoring='accuracy'):    
        melhor = 0
        # labels = ['1', '2']  # respostas
        labels = respostas
        modelos = []
        
        # Definir os scorers
        scorers = {
            'accuracy': make_scorer(accuracy_score),
            'f1_score': make_scorer(f1_score, average='weighted', zero_division=1),  # zero_division=1 para F1-score
            'recall': make_scorer(recall_score, average='weighted', zero_division=1),  # zero_division=1 para Recall
            'precision': make_scorer(precision_score, average='weighted', zero_division=1)  # zero_division=1 para Precisão
        }
        
        # Preparar validação cruzada
        kf = KFold(n_splits=cv, shuffle=True, random_state=42)
        
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
            y_pred_test = cloned_model.predict(X_test)
            
            # Calcular as métricas no conjunto de treino
            accuracy = accuracy_score(y_test, y_pred_test)
            f1 = f1_score(y_test, y_pred_test, average='weighted', zero_division=1)
            recall = recall_score(y_test, y_pred_test, average='weighted', zero_division=1)
            precision = precision_score(y_test, y_pred_test, average='weighted', zero_division=1)
            
            # Armazenar a matriz de confusão e o relatório de classificação
            cm = confusion_matrix(y_test, y_pred_test)
            cr = classification_report(y_test, y_pred_test, target_names=labels)
            
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

        
    # recebe um objeto do tipo dataset, com o dataset aberto, puxa da casse arquivo
    def valida_sem_salvar_modelo(dataset, nome_classe, colums_list):
        score = []
        min_count = dataset[nome_classe].value_counts().min()
        dataset = dataset.groupby(nome_classe).sample(n=min_count, random_state=4)
        # a princípio vou utilizar as colunas conforme o algoritmo genético soltar
        colunas_iniciais = [colums_list]
        for i in range(len(colunas_iniciais), 0, -1):
            colunas_atualizadas = colunas_iniciais[:i]  # Seleciona as primeiras i colunas
            dataset_sem_classe = dataset[colunas_atualizadas]  # Seleciona o dataset com as colunas atualizadas
            
            # Definir o modelo de machine learning
            algoritmoML = DecisionTreeClassifier(max_depth=5)
            
            # Avaliar o modelo com validação cruzada
            # scores, best_model = evaluate_model_with_cross_validation(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')
            scores = cross_val_score(algoritmoML, dataset_sem_classe, dataset, cv=10, scoring="f1_macro")
            score.append(scores.mean())
            # Exibir o F1-score e a quantidade de colunas utilizadas na iteração atual
            print(f"Quantidade de atributos: {len(colunas_atualizadas)}, F1_score: {scores.mean()}")
        for i in score:
            print(i)
            
    # Função para salvar o melhor modelo
    def selec_best_model(model):
        # Verificar se o arquivo existe
        with open('modelo_treinado.pkl', 'wb') as file:
            pickle.dump(model, file)


    def valida_salvando_modelo(self, dataset, nome_classe):
        dataset_ = dataset
        dataset_classe = dataset_[nome_classe]
        dataset_sem_classe = dataset_.drop(columns=[nome_classe])
        algoritmoML = DecisionTreeClassifier(max_depth=5)
        scores, best_model = self.evaluate_model_with_cross_validation(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')
        self.selec_best_model(best_model)
        # Exibir o F1-Score
        print(f"F1_score: {scores}")