"""
Functionality for preprocessing event vectors for ML model
"""
import numpy as np
import math

# Default standardised event vector for classification
STANDARD_EVENT_LENGTH = 20

def standardise(arr, n=STANDARD_EVENT_LENGTH):
    """
    Standardise event to n length vector by shrinking or expanding
    Parameters: array_like : arr : event vector to be standardised
                int : n (optional) : standardisation length
    """
    if arr.ndim == 1: arr = arr[None, :]
    ret = np.zeros((arr.shape[0], n))

    def split(x):
        i = math.floor(abs(x)/2)
        return i, abs(x)-i

    for ai in range(arr.shape[0]):
        a = (lambda z:z[~np.isnan(z)])(arr[ai, :])
        i,j = split(n-len(a))
        if len(a) < n:
            ret[ai] = np.hstack([np.repeat(np.array([a[0]]), i), a, np.repeat(np.array([a[-1]]),j)])
        elif len(a) == n:
            ret[ai] = a
        else:
            ret[ai] = a[i:-j]
    
    return ret

def normalise(X): 
    """
    Normalise vector to between 0,1
    """
    return (X-X.min(axis=1)[:,None])/(X.max(axis=1)-X.min(axis=1))[:,None]