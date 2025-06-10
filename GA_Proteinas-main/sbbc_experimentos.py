import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer, recall_score, accuracy_score, precision_score

# Carregar o dataset
dataset = pd.read_csv("BaseDepressao.csv")

# Separar a variável alvo
coluna_alvo = "Diagnostico_Depressao"
y = dataset[coluna_alvo]

# Lista de índices das colunas ordenadas (exemplo que você deu)
indices_ordenados = [16, 29, 12, 21, 27, 38, 25, 39, 22, 15, 20, 33, 6, 19, 7, 11, 17]

# Lista com os nomes reais das colunas
nomes_colunas = dataset.columns.tolist()
nomes_colunas.remove(coluna_alvo)

# Validação: índice não pode extrapolar número de colunas
assert max(indices_ordenados) < len(nomes_colunas), "Tem índice fora do range de colunas!"

# Loop para testar de 1 até o máximo de colunas
print("Quantidade | Acurácia | F1-score | Precisão | Recall")

resultados = []
for top_k in range(1, len(indices_ordenados) + 1):
    colunas_top_k = [nomes_colunas[i] for i in indices_ordenados[:top_k]]
    X = dataset[colunas_top_k]
    
    modelo = DecisionTreeClassifier(max_depth=5)
    
    # Calcula todas as métricas com cross-validation
    acc = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(accuracy_score)).mean()
    f1 = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(f1_score, average='macro')).mean()
    prec = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(precision_score, average='macro', zero_division=1)).mean()
    rec = cross_val_score(modelo, X, y, cv=10, scoring=make_scorer(recall_score, average='macro')).mean()
    
    resultados.append((top_k, acc, f1, prec, rec))
    
    print(f"{top_k:^10} | {acc:.4f}  | {f1:.4f}  | {prec:.4f}   | {rec:.4f}")

# (Opcional) Salvar em CSV
# pd.DataFrame(resultados, columns=["Quantidade", "Accuracy", "F1", "Precision", "Recall"]).to_csv("metricas_resultados.csv", index=False)
