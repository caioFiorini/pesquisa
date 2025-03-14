import numpy as np
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.metrics import make_scorer, accuracy_score, f1_score, recall_score, precision_score, confusion_matrix, classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.base import clone
from sklearn.base import clone
from sklearn.model_selection import KFold

def evaluate_model_with_cross_validation(model, X_rus, y_rus, cv=10, metric='accuracy'):
    
    melhor=0
    labels = ['1', '2'] #?
    labels2 = [1, 2] #?
    
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
        X_train, X_test = X_rus[train_index], X_rus[test_index]
        y_train, y_test = y_rus[train_index], y_rus[test_index]
        
        # Clonar o modelo para evitar o ajuste acumulativo
        cloned_model = clone(model)
        
        # Treinar o modelo
        cloned_model.fit(X_train, y_train)
        
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
        
    
    # Calcular as médias das métricas
    accuracies = [result['accuracy'] for result in results]
    f1_scores = [result['f1_score'] for result in results]
    recalls = [result['recall'] for result in results]
    precisions = [result['precision'] for result in results]
    
    mean_accuracy = np.mean(accuracies)
    mean_f1_score = np.mean(f1_scores)
    mean_recall = np.mean(recalls)
    mean_precision = np.mean(precisions)
       
    # Encontrar o melhor modelo com base na métrica escolhida
    if metric == 'accuracy':
         best_fold_idx = np.argmax(accuracies)
    elif metric == 'f1_score':
        best_fold_idx = np.argmax(f1_scores)
    elif metric == 'recall':
        best_fold_idx = np.argmax(recalls)
    elif metric == 'precision':
        best_fold_idx = np.argmax(precisions)
    else:
        raise ValueError(f"Metric '{metric}' not supported. Choose from: 'accuracy', 'f1_score', 'recall', 'precision'.")
    
    best_model = clone(model)
    best_model.fit(X_rus, y_rus)
    
    # Imprimir os resultados médios
    print(f'Mean Accuracy: {mean_accuracy:.4f}')
    print(f'Mean F1-Score: {mean_f1_score:.4f}')
    print(f'Mean Recall: {mean_recall:.4f}')
    print(f'Mean Precision: {mean_precision:.4f}')
    
    return results, best_model