from threading import Thread

class SoundRecorder(Thread):
    def __init__(self, process, sink, sample_rate, recording_duration, logging, overlap_duration):
        super(SoundRecorder,self).__init__()
        self.process = process
        self.sink = sink
        self.sample_rate = sample_rate
        self.recording_duration = recording_duration
        self.logging = logging
        self.overlap_duration = overlap_duration

    def run(self):
        start_time = 0
        while True:
            try :
                output = self.process(self.recording_duration, self.sample_rate, self.logging,self.overlap_duration)
                self.sink.add(output)
            except Exception as e:
                logging.error("Failed to record")