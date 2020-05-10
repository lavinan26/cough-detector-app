
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import random
from sklearn.svm import SVC
import pickle
import librosa
def preProcess(signal,logging):
    frame_length = 512
    frame_step = 358
    NFFT = 512
    nfilt = 40
    num_ceps = 40
    cep_lifter = 22
    sample_rate = 22050
    low_freq_mel = 0
    high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))
    mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
    hz_points = (700 * (10**(mel_points / 2595) - 1))
    bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)
    fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1]) 
        f_m = int(bin[m])      
        f_m_plus = int(bin[m + 1]) 

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    def extract_features(signal, received_rate):
        signal_length = len(signal)
        num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length)) / frame_step))
        pad_signal_length = num_frames * frame_step + frame_length
        z = numpy.zeros((pad_signal_length - signal_length))
        pad_signal = numpy.append(signal, z)
        indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
        frames = pad_signal[indices.astype(numpy.int32, copy=False)]
        frames *= numpy.hamming(frame_length)
        mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))
        pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
        fbank_energies = numpy.dot(pow_frames, fbank.T)
        fbank_energies = numpy.where(fbank_energies == 0, numpy.finfo(float).eps, fbank_energies)
        fbank_energies = 20 * numpy.log10(fbank_energies)
        fbank_compress = dct(fbank_energies, type=2, axis=1, norm='ortho')
        fbank_compress = fbank_compress[:, 0 : num_ceps]
        (nframes, ncoeff) = fbank_compress.shape
        n = numpy.arange(ncoeff)
        lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
        fbank_deemphasize = fbank_compress * lift
        mfcc = fbank_deemphasize - (numpy.mean(fbank_deemphasize, axis=0) + 1e-8)
        mfcc_scaler = StandardScaler()
        mfcc_scaler.fit(mfcc.T)
        mfcc_scaled = mfcc_scaler.transform(mfcc.T)
        pca = PCA(.99)
        pca.fit(mfcc_scaled)
        pca_mfcc = pca.transform(mfcc_scaled)
        ei = pca.components_
        reconst_mfcc = np.dot(ei.T,pca_mfcc.T)
        mse = np.square(reconst_mfcc.T-mfcc_scaled).mean()
        var = np.var(mfcc_scaled)
        retain = mse/var
        if retain > 0.01:
            print ("99% not retained for audio " + str(audio))
        feature_set1 = mfcc.T.mean(axis = -1)
        feature_set2 = numpy.linalg.norm(pca_mfcc,axis = -1)
        feature_set = numpy.hstack((feature_set1,feature_set2))
        return feature_set
    features = extract_features(signal,22050)
    
    return features