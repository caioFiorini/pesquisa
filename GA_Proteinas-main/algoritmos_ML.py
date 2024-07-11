from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import tree

class AlgoritmosML:
    
    def __init__(self, nome_classificador, lista_parametros):
        if (nome_classificador == 'SVM') :
            self.SVM(C = lista_parametros[1],
            kernel = lista_parametros[1],
            degree = lista_parametros[1],
            gamma = lista_parametros[1],
            coef0 = lista_parametros[1],
            shrinking = lista_parametros[1],
            probability = lista_parametros[1],
            tol = lista_parametros[1],
            cache_size = lista_parametros[1],
            class_weight = lista_parametros[1],
            verbose = lista_parametros[1],
            max_iter = lista_parametros[1],
            decision_function_shape = lista_parametros[1],
            break_ties = lista_parametros[1],
            random_state = lista_parametros[1])
    
    def KNN(
            n_neighbors=5, 
            weights='uniform', 
            algorithm='auto', 
            leaf_size=30, 
            p=2, 
            metric='minkowski',
            metric_params= None,
            n_jobs=None
            ): 
        knn = KNeighborsClassifier(
            n_neighbors=n_neighbors, 
            weights=weights, 
            algorithm=algorithm, 
            leaf_size=leaf_size,
            p=p,
            metric=metric,
            metric_params=metric_params,
            n_jobs=n_jobs
            )
        return knn 
    
    def SVM(
            C = 1.0,
            kernel ='rbf',
            degree = 3,
            gamma = 'scale',
            coef0 = 0.0,
            shrinking = True,
            probability = False,
            tol = 1e-3,
            cache_size = 200,
            class_weight = None,
            verbose = False,
            max_iter = -1,
            decision_function_shape = 'ovr',
            break_ties = False,
            random_state = None
            ):
        svc = SVC(
                  C=C,
                  kernel=kernel,
                  degree=degree,
                  gamma=gamma,
                  coef0=coef0,
                  shrinking=shrinking,
                  probability=probability,
                  tol=tol,
                  cache_size=cache_size,
                  class_weight=class_weight,
                  verbose=verbose,
                  max_iter=max_iter,
                  decision_function_shape=decision_function_shape,
                  break_ties=break_ties,
                  random_state=random_state
                  )
        return svc
    
    def DecisionTree(criterion='gini', 
                     splitter='best', 
                     max_depth=None, 
                     min_samples_split=2, 
                     min_samples_leaf=1, 
                     min_weight_fraction_leaf=0.0, 
                     max_features=None, 
                     random_state=None, 
                     max_leaf_nodes=None, 
                     min_impurity_decrease=0.0, 
                     class_weight=None, 
                     ccp_alpha=0.0
                    ):
            arvore = tree.DecisionTreeClassifier(criterion=criterion,
                                                 splitter=splitter,
                                                 max_depth=max_depth,
                                                 min_samples_split=min_samples_split,
                                                 min_samples_leaf=min_samples_leaf,
                                                 min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                 max_features=max_features,
                                                 random_state=random_state,
                                                 max_leaf_nodes=max_leaf_nodes,
                                                 min_impurity_decrease=min_impurity_decrease,
                                                 class_weight=class_weight,
                                                 ccp_alpha=ccp_alpha)
            return arvore
