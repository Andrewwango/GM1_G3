import numpy as np
from constants import *
from events import Events
import pickle, os, joblib
from ml_training.preprocessing import normalise, standardise
from sklearn.naive_bayes import GaussianNB

class Classifier(GaussianNB):
    def predict(self, X):
        if type(X) is list: X = np.array(X)
        if X.ndim == 1: X = X.reshape(1,-1)
        return super().predict(normalise(standardise(X, 20)))

training_data = pickle.load(open('ml_training/event_classification_training_data', 'rb'))
classifier = Classifier().fit(*training_data)

def detectEventType(event, method="ml"):
    return classify_simple(event) if method=='simple' else classify_ml(event)

def classify_simple(event):
    change = event.net_change()
    short_time = event.time_taken() <= SHORT_TIME_SECS
    if change > STEPCHANGE_THRESH and short_time:
        return Events.STEPUP
    elif change < -STEPCHANGE_THRESH and short_time:
        return Events.STEPDOWN
    elif short_time:
        return Events.GLITCH
    elif not short_time:
        return Events.EATING

def classify_ml(event):
    return Events(classifier.predict(event.buffer.buffer))