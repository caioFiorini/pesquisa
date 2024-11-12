import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score, recall_score, precision_score, make_scorer
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_score
from sklearn import tree
import matplotlib.pyplot as plt
import pickle

# Função para realizar cross-validation e avaliar o modelo
def evaluate_model_with_cross_validation(model, X_rus, y_rus, cv=10, scoring='accuracy'):    
    labels = ['1', '2']  # respostas
    modelos = []
    results = []
    kf = KFold(n_splits=cv)

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
    
    # Selecionar o melhor modelo com base no F1-score
    f1_scores = [result['f1_score'] for result in results]
    id_melhor_modelo = f1_scores.index(max(f1_scores))
    
    best_model = modelos[id_melhor_modelo]
    best_score = max(f1_scores)
    return best_score, best_model

# Função para salvar o melhor modelo
def selec_best_model(model):
    with open('modelo_treinado.pkl', 'wb') as file:
        pickle.dump(model, file)

# Carregar o dataset
dataset = pd.read_csv("BaseColesterol_posprocessFinal.csv")
score = []
min_count = dataset['Colesterol_Alto'].value_counts().min()
dataset = dataset.groupby("Colesterol_Alto").sample(n=min_count, random_state=4)

# Separar os dados de entrada e saída
dataset_classe = dataset["Colesterol_Alto"]

# Lista de todas as colunas desejadas
colunas_iniciais = [
    'P051_2.0', 'Consumo Leite', 'P051_1.0', 'Consumo Frango/Galinha', 'Consumo Refrigerante', 'Hidroginástica',
    'Exercício Físico Últimos 3 Meses', 'Musculação', 'Frequência Exercício Físico', 'Consumo Frutas', 'Aula de dança', 
    'Consumo Frutas.1', 'Futebol', 'Frequência Bebida Alcoólica', 'Consumo Verduras/Legumes', 'Consumo Peixe', 'Voleibol',
    'Consumo Leite.1', 'Consumo Bebida Alcoólica', 'Caminhada (não vale para o trabalho)', 'Bicicleta ou bicicleta ergométrica',
    'Tênis', 'Diabetes', 'Corrida em esteira', 'Consumo Carne Vermelha', 
    'Caminhada em esteira', 'Outro', 'Ignorado', 'Consumo Alimentos Fritos', 'Histórico Consumo Tabaco', 'Genero Masculino', 
    'Faixa IMC', 'Consumo Sal', 'Consumo Atual Tabaco', 'Corrida ou cooper', 'Ginástica aeróbica/spinning/step/jump',
    'Basquetebol', 'Consumo Doces', 'Natação', 'Genero Feminino', 'Ginástica localizada/pilates/alongamento ou ioga', 
    'Não Diabetes', 'Artes marciais e luta', 'IMC', 'Consumo Suco'
]

# Loop para diminuir a quantidade de colunas a cada iteração
for i in range(len(colunas_iniciais), 0, -1):
    colunas_atualizadas = colunas_iniciais[:i]  # Seleciona as primeiras i colunas
    dataset_sem_classe = dataset[colunas_atualizadas]  # Seleciona o dataset com as colunas atualizadas
    
    # Definir o modelo de machine learning
    algoritmoML = DecisionTreeClassifier(max_depth=5)
    
    # Avaliar o modelo com validação cruzada
    # scores, best_model = evaluate_model_with_cross_validation(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')
    scores = cross_val_score(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring="f1_macro")
    score.append(scores.mean())
    # Exibir o F1-score e a quantidade de colunas utilizadas na iteração atual
    print(f"Quantidade de atributos: {len(colunas_atualizadas)}, F1_score: {scores.mean()}")
    
    # Plotar a árvore de decisão
    # plt.figure(figsize=(24, 12))
    # tree.plot_tree(best_model, feature_names=dataset_sem_classe.columns, filled=True)
    # plt.show()
    
    # Salvar o melhor modelo
    # selec_best_model(best_model)
    
for i in score:
    print(i)