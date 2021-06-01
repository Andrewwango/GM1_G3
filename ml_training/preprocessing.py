import numpy as np
import math

def standardise(arr, n):
    if arr.ndim == 1: arr = arr[None, :]
    ret = np.zeros((arr.shape[0], n))
    def split(x):
        x = abs(x)
        i = math.floor(x/2)
        return i, x-i
    for ai in range(arr.shape[0]):
        a = arr[ai, :]
        a = a[~np.isnan(a)]
        i,j = split(n-len(a))
        if len(a) < n:
            ret[ai] = np.hstack([np.repeat(np.array([a[0]]), i), a, np.repeat(np.array([a[-1]]),j)])
        elif len(a) == n:
            ret[ai] = a
        else:
            ret[ai] = a[i:-j]
    return ret

def normalise(X): return (X-X.min(axis=1)[:,None])/(X.max(axis=1)-X.min(axis=1))[:,None]