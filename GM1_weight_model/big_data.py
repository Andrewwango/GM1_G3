"""
Demonstration of how to a nueral network can be trained to estimate the BMR of a patient from a demo dataset

"""

from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from matplotlib import pyplot
from pandas import DataFrame


#features are age, wieght, exercise level

features, BMR = make_regression(n_samples=100, n_features=3, noise=0.1)
BMR = BMR*5


clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(5, 2), random_state=1,max_iter=1000)
clf.fit(features, BMR)

#predict someones BMR with age = 80, weight = 60 kg, excersize level = 6
print (clf.predict([[80, 60,6]]))
