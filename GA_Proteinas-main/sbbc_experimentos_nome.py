import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer, recall_score, accuracy_score, precision_score

# Carregar o dataset
dataset = pd.read_csv("BaseDepressao.csv")

# Separar a variável alvo
coluna_alvo = "Diagnostico_Depressao"
y = dataset[coluna_alvo]

# Lista de nomes das colunas ordenadas (exemplo: substitua pelas suas)
colunas_ordenadas =  ['Sexo', 'Apoio_Familiar', 'Tipo_de_Trabalho', 'Pratica_Exercicio', 'Procura_Atendimento_Saude', 'Problemas_Sono', 'IMC', 'doencas_cronicas', 'moradia_vulneravel', 'tempo_total_exercicio', 'frequencia_exercicio', 'Consumo de Leguminosas', 'Consumo de Carnes', 'Consumo de Verduras e Legumes', 'Consumo de Frutas', 'Consumo de Laticinios', 'Consumo de Refrigerantes', 'Consumo de Salgadinhos e Biscoitos Salgados', 'Consumo de Paes Industrializados', 'Consumo de Molhos Industrializados', 'Substituicao de Refeicoes por Lanches Rapidos']



# Validação: todas as colunas devem existir no dataset
for col in colunas_ordenadas:
    assert col in dataset.columns, f"Coluna '{col}' não existe no dataset!"

# Loop para testar de 1 até o máximo de colunas
print("Quantidade | Acurácia | F1-score | Precisão | Recall")
print("-" * 55)

resultados = []
for top_k in range(1, len(colunas_ordenadas) + 1):
    colunas_top_k = colunas_ordenadas[:top_k]
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
