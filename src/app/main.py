import sys
sys.path.append("./")
from threading import Thread
import logging
from tensorflow.keras.models import load_model
from modules.soundRecorder import SoundRecorder
from modules.soundReceiver import SoundReceiver
from modules.responder import Responder
from modules.processor import Processor
from recordSound.soundRecorder import record
from process.preProcessor import PreProcessing
from process.detector import infer
from respond.responder import respond

preprocess = PreProcessing()

#Load model in the below line
# If tflite model
model_file = open("model\\tflite_model.tflite","rb")
model = model_file.read()
model_file.close()

# If CNN model
#model = load_model("src\\model\\model_CNN.h5")

logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', level=logging.INFO)
receiver = SoundReceiver(logging = logging,overlap_duration = 2, sample_rate = 22050)
source = SoundRecorder(process = record, sink = receiver,sample_rate = 22050, recording_duration = 5,logging = logging, overlap_duration = 2)
responder = Responder(logging = logging, respond = respond)
processor = Processor(source = receiver, sink = responder, pre_processor = preprocess, detector = infer, logging = logging, model = model)
source.setDaemon = True
processor.setDaemon = True
source.start()
processor.start()

#while True:
#    a = 2
    #logging.info(receiver.queue)