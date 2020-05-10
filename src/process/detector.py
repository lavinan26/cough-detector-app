import numpy as np
import pickle
from sklearn.svm import SVC
def infer(signal,logging,model):
    result = model.predict([signal])[0]
    return result