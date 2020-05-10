import sounddevice as sd
import numpy as np

def record(audio_duration,sample_rate,logging,overlap_duration):
    recording_samples = int((audio_duration-overlap_duration)* sample_rate)
    audio = sd.rec(recording_samples,samplerate=sample_rate, channels= 1)
    #logging.info("recording")
    sd.wait()
    return audio