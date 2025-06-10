import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer, recall_score, accuracy_score, precision_score

# Carregar o dataset
dataset = pd.read_csv("dataset_balanceado_final.csv") 

# Separar a variável alvo
coluna_alvo = "classe"
y = dataset[coluna_alvo]
dataset.drop(coluna_alvo, axis=1, inplace=True)

X = dataset

# Loop para testar de 1 até o máximo de colunas
print("Acurácia | F1-score | Precisão | Recall")

modelo = DecisionTreeClassifier(max_depth=5,random_state=42)
    
# Calcula todas as métricas com cross-validation
acc = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(accuracy_score)).mean()
f1 = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(f1_score, average='macro')).mean()
prec = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(precision_score, average='macro', zero_division=1)).mean()
rec = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(recall_score, average='macro')).mean()
    
print(f"{acc:.4f}  | {f1:.4f}  | {prec:.4f}   | {rec:.4f}")

# (Opcional) Salvar em CSV
# pd.DataFrame(resultados, columns=["Quantidade", "Accuracy", "F1", "Precision", "Recall"]).to_csv("metricas_resultados.csv", index=False)
