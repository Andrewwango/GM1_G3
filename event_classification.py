"""
Classes and functions to classify events
"""
import numpy as np
from constants import *
from events import Events
import pickle
from ml_training.preprocessing import normalise, standardise, STANDARD_EVENT_LENGTH
from sklearn.naive_bayes import GaussianNB

class Classifier(GaussianNB):
    """
    Class for fitting according to Gaussian Naive Bayes
    and predicting with preprocess step
    Methods: predict
    """
    def predict(self, X):
        """
        Predict class from new sample event(s)
        Parameters: array_like : X : new samples to be classified
        Returns: array_like : class labels
        """
        if type(X) is list: X = np.array(X)
        return super().predict(normalise(standardise(X.reshape(1,-1) if X.ndim == 1 else X, STANDARD_EVENT_LENGTH)))

# On initialisation: load training data and fit classifier
training_data = pickle.load(open('ml_training/event_classification_training_data', 'rb'))
classifier = Classifier().fit(*training_data)

def detectEventType(event, method="ml"):
    """
    Select classifier to classify events
    Parameters: Events : event : incoming event to be classified
                str : method (optional): method of classification : simple or machine learning
    Returns: int : label of classified event
    """
    return classify_simple(event) if method=='simple' else classify_ml(event)

def classify_simple(event):
    """
    Classify event according to simple thresholding
    Parameters: Events : event : incoming event to be classified
    Returns: int : label of classified event    
    """
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
    """
    Classify event according to ML model
    Parameters: Events : event : incoming event to be classified
    Returns: int : label of classified event 
    """
    return Events(classifier.predict(event.buffer.buffer))