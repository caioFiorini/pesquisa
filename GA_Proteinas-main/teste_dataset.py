import pandas as pd
from sklearn import tree
from sklearn.metrics import make_scorer, accuracy_score, f1_score, recall_score, precision_score, confusion_matrix, classification_report
from sklearn.model_selection import KFold, cross_val_score

dataset = pd.read_csv("BaseColesterol_posprocessFinal.csv")

classe = dataset["Colesterol_Alto"]
coluna_teste = dataset[[]]



model = tree.DecisionTreeClassifier(max_depth=5)

score = cross_val_score(model, coluna_teste, classe, cv=10, scoring="f1_macro")
# for i in score:
#     print(i)
print(f"{score.mean()}")

