import numpy as np
from scipy.signal import spectrogram


class PreProcessing():
    def __init__(self,sampling_rate=22050):
        self.sampling_rate = sampling_rate

    def __call__(self,audio_array,logging):
        audio_array = np.squeeze(audio_array)
        spectrum = self.spect(audio_array)
        normal_spectrum = self.normalize_spectrum(spectrum)
        return normal_spectrum

    def spect(self,audio):
        sampling_rate = self.sampling_rate
        NFFT = 512
        f, t, Sxx = spectrogram(x=audio,fs=sampling_rate,window=np.hamming(NFFT),nfft=NFFT,noverlap=int(NFFT/3),nperseg=NFFT,mode='magnitude')
        spectrum = 20*np.log10(Sxx)
        spectrum = spectrum.ravel().reshape(257,321,1)
        return spectrum

    def normalize_spectrum(self,spectrum):
        return (spectrum - np.mean(spectrum))/np.std(spectrum)