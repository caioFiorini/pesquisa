import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score




dataset = pd.read_csv("AVCBalanceado-AG.csv")
# print(dataset.columns)

dataset_classe = dataset["AVC"]
dataset_sem_classe = dataset[["Gênero"]]
# print(dataset_sem_classe)
# dadosTreino, dadosTeste, respostaTreino, respostaTeste = train_test_split(dadosSemResposta, dadosComResposta, test_size = 0.20, random_state = 0)

algoritmoML = DecisionTreeClassifier(max_depth=5)
scores = cross_val_score(algoritmoML, dataset_sem_classe, dataset_classe, cv=10, scoring='f1_macro')
for i in scores:
    print(i)
scores = scores.mean()
print(f"F1_score: {scores}")
