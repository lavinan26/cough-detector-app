from threading import Thread

class Processor(Thread):
    def __init__(self, source, sink, pre_processor, detector,logging, model):
        super(Processor,self).__init__()
        self.source = source
        self.sink = sink
        self.pre_processor = pre_processor
        self.detector = detector
        self.logging = logging
        self.model = model

    def run(self):
        while True:
            try:
                signal = self.source.dequeue()
                if signal is not None :
                    feature = self.pre_processor(signal,self.logging)
                    result = self.detector(feature,self.logging,self.model)
                    self.sink.respond(result,self.logging)
            except Exception as e:
                #logging.error("Failed to process")
                self.logging.error(e)
