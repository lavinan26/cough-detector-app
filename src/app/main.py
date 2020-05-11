import sys
sys.path.append("./")
from threading import Thread
import logging
from tensorflow.keras.models import load_model
from src.modules.soundRecorder import SoundRecorder
from src.modules.soundReceiver import SoundReceiver
from src.modules.responder import Responder
from src.modules.processor import Processor
from src.recordSound.soundRecorder import record
from src.process.preProcessor import PreProcessing
from src.process.detector import infer
from src.respond.responder import respond

preprocess = PreProcessing()

#Load model in the below line
model = load_model("src\\model\\model_CNN.h5")
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