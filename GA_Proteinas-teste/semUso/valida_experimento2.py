import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score, confusion_matrix

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

# Configurar validação cruzada
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Variáveis para armazenar as métricas
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []
confusion_matrices = []

# Executar validação cruzada
for train_index, test_index in skf.split(dataset_sem_classe, dataset_classe):
    # Dividir os dados em treino e teste
    X_train, X_test = dataset_sem_classe.iloc[train_index], dataset_sem_classe.iloc[test_index]
    y_train, y_test = dataset_classe.iloc[train_index], dataset_classe.iloc[test_index]
    
    # Treinar o modelo
    algoritmoML.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = algoritmoML.predict(X_test)
    
    # Calcular métricas
    accuracy_list.append(accuracy_score(y_test, y_pred))
    precision_list.append(precision_score(y_test, y_pred, average='macro'))
    recall_list.append(recall_score(y_test, y_pred, average='macro'))
    f1_list.append(f1_score(y_test, y_pred, average='macro'))
    confusion_matrices.append(confusion_matrix(y_test, y_pred))

# Exibir as métricas médias
print(f"Average Accuracy: {sum(accuracy_list) / len(accuracy_list):.4f}")
print(f"Average Precision: {sum(precision_list) / len(precision_list):.4f}")
print(f"Average Recall: {sum(recall_list) / len(recall_list):.4f}")
print(f"Average F1 Score: {sum(f1_list) / len(f1_list):.4f}")

# Exibir a matriz de confusão acumulada
print("\nConfusion Matrices (per fold):")
for i, cm in enumerate(confusion_matrices):
    print(f"Fold {i+1}:\n{cm}")
