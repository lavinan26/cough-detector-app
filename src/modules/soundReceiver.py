import numpy as np

class SoundReceiver:
    def __init__(self,logging,overlap_duration,sample_rate):
        self.queue = []
        self.overlap = np.zeros([overlap_duration*sample_rate,1])
        self.logging = logging
        self.first_overlap_sample = -1*(overlap_duration*sample_rate)
    
    def enqueue(self,audio):
        self.queue.append(audio)

    def dequeue(self):
        try:
            return self.queue.pop(0)
        except Exception:
            pass
            #self.logging.error("unable to deqeue")

    def add(self,audio):
        joined_audio = np.vstack((self.overlap,audio))
        self.enqueue(joined_audio)
        self.overlap = audio[self.first_overlap_sample:]
