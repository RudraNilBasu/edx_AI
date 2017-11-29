import numpy as NUM_PY
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression





def load_data_samples(input_file_example):
    datasetSamples = NUM_PY.genfromtxt(input_file_example, delimiter=',', skip_header=1, names=None)

    X_Data = datasetSamples[:, :-1]
    Y_Data = datasetSamples[:, -1]
    return (X_Data, Y_Data)

X_DataSample, Y_data_Label = load_data_samples('input3.csv')

X_training_data, X_testing_data, y_training_data, y_testing_data = train_test_split(X_DataSample, Y_data_Label, test_size=0.4, random_state=42)
estimator_svm_values = svm.SVC()

parameters_forProcessing = {'kernel': ('linear',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
gridSearch_CLF = GridSearchCV(estimator_svm_values, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

gridSearch_BsetEstimator_svc = gridSearch_CLF.best_estimator_

print gridSearch_BsetEstimator_svc.score(X_testing_data, y_testing_data)

# SVM with Polynomial Kernel.
parameters_forProcessing = {'kernel': ('poly',), 'C': [0.1, 1, 3], 'degree': [4, 5, 6], 'gamma': [0.1, 1]}

gridSearch_CLF = GridSearchCV(estimator_svm_values, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

svc_poly = gridSearch_CLF.best_estimator_

print svc_poly.score(X_testing_data, y_testing_data)

#SVM with RBF Kernel.
parameters_forProcessing = {'kernel': ('rbf',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}

gridSearch_CLF = GridSearchCV(estimator_svm_values, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

gridSearch_svc_rbf = gridSearch_CLF.best_estimator_

print gridSearch_svc_rbf.score(X_testing_data, y_testing_data)

#Logistic Regression.
parameters_forProcessing = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
estimator_logisticRegression = LogisticRegression()
gridSearch_CLF = GridSearchCV(estimator_logisticRegression, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

svc_lr = gridSearch_CLF.best_estimator_

print svc_lr.score(X_testing_data, y_testing_data)

#k-Nearest Neighbors. Try values of n_neighbors = [1, 2, 3, ..., 50] and leaf_size = [5, 10, 15, ..., 60].
parameters_forProcessing = {'n_neighbors': xrange(1, 51), 'leaf_size': xrange(5, 61, 5)}
kNeighbors_estimator = KNeighborsClassifier()
gridSearch_CLF = GridSearchCV(kNeighbors_estimator, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

gridSearch_svc_knn = gridSearch_CLF.best_estimator_

print gridSearch_svc_knn.score(X_testing_data, y_testing_data)



#Decision Trees. Try values of max_depth = [1, 2, 3, ..., 50] and min_samples_split = [2, 3, 4, ..., 10].
parameters_forProcessing = {'max_depth': xrange(1, 51), 'min_samples_split': xrange(2, 11)}
decisionTreeClassifierEstimator_dt = DecisionTreeClassifier()
gridSearch_CLF = GridSearchCV(decisionTreeClassifierEstimator_dt, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

decisionTreeEstimator = gridSearch_CLF.best_estimator_

print decisionTreeEstimator.score(X_testing_data, y_testing_data)



#Random Forest.  Try values of max_depth = [1, 2, 3, ..., 50] and min_samples_split = [2, 3, 4, ..., 10].
parameters_forProcessing = {'max_depth': xrange(1, 51), 'min_samples_split': xrange(2, 11)}
randomForestClassifierEstimator = RandomForestClassifier()
gridSearch_CLF = GridSearchCV(randomForestClassifierEstimator, parameters_forProcessing, cv=5)
gridSearch_CLF.fit(X_training_data, y_training_data)

print gridSearch_CLF.best_estimator_
print gridSearch_CLF.best_score_

rainForestEstimator = gridSearch_CLF.best_estimator_

print rainForestEstimator.score(X_testing_data, y_testing_data)

