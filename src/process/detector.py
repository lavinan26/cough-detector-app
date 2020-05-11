import numpy as np

def infer(signal,logging,model):
    signal = np.expand_dims(signal,axis=0)
    prediction = model.predict(x = signal,batch_size = 1)
    prediction = np.round(prediction)
    if prediction:
        result = "cough"
    else:
        result = "non_cough"
    #return result as either "cough" or "non_cough"
    return result