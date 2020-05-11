import numpy as np
import tensorflow as tf

def infer(signal,logging,model):
    input_data = np.expand_dims(signal,axis=0)
    interpreter = tf.lite.Interpreter(model_content=model)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    tflite_results = interpreter.get_tensor(output_details[0]['index'])

    prediction = np.round(tflite_results)
    if prediction:
        result = "cough"
    else:
        result = "non_cough"
    #return result as either "cough" or "non_cough"
    return result