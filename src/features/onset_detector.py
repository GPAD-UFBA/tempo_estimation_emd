import librosa
import librosa.display
import numpy as np
from src.data.data_loader import audio_loader


class OnsetDetector:
    """
    Onset parameters
    """

    def __init__(self):
        self.n_fft = 1024
        self.lag = 2
        self.n_mels = 138
        self.fmin = 27.5
        self.fmax = 16000.
        self.max_size = 3
    
    def odf_sf(self,signal,sample_rate):
        """
        Compute a spectral flux onset strength envelope.
        """
        hop_length = int(librosa.time_to_samples(1./200, sr=sample_rate))

        S = librosa.feature.melspectrogram(y=signal, sr=sample_rate, n_fft=self.n_fft,
                                    hop_length=hop_length,
                                    fmin=self.fmin,
                                    fmax=self.fmax,
                                    n_mels=self.n_mels)
        
        odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                        sr=sample_rate,
                                        hop_length=hop_length,
                                        lag=self.lag, max_size=self.max_size)
        
        return odf_sf, hop_length
    def odf(self,signal,sample_rate):
        """
        Detects the onsets of the audio and returns the onset times.
        """
        
        odf_sf, hop_length = self.odf_sf(signal,sample_rate)

        onset_sf = librosa.onset.onset_detect(onset_envelope=odf_sf,
                                        sr=sample_rate,
                                        hop_length=hop_length,
                                        units='time')

        return onset_sf

if __name__ == "__main__":
    y, sr = audio_loader('/data/audio/snare_example.wav')
    onset_detector = OnsetDetector()
    onset_detector.odf(y, sr)   



