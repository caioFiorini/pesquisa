from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

class AlgoritmosML:
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