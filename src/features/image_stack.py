import numpy as np


import librosa



class ImageStack:


    def __init__(self,y,sr):      


        self.y = y
        self.sr = sr
        


        self.hop_length = int(librosa.time_to_samples(1./200, sr=sr))


        self.lag = 2


        self.max_size = 3
    

    def create_melspectrogram(self):


        self.s = librosa.feature.melspectrogram(y=self.y, sr=self.sr)


        self.s_db = librosa.power_to_db(self.s, ref=np.max)
    


        return self.s_db 


    def get_superflux(self):


        self.odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(self.s, ref=np.max),

                                      sr=self.sr,


                                      hop_length=self.hop_length,


                                      lag=self.lag, max_size=self.max_size)
        return self.odf_sf
    

    def signal_duration(self):


        return librosa.get_duration(y=self.y,sr=self.sr)
    


    def odf_sample_rate(self):


        return len(self.odf_sf)/self.signal_duration()
    

    def superflux_downsampled(self):
        superflux_samplerate = len(self.odf_sf)/self.signal_duration()
        return librosa.resample(self.odf_sf.reshape(1,-1), 

                                orig_sr=superflux_samplerate, 
                                target_sr=self.odf_sample_rate())
        

    def create_superflux_image(self):

        self.get_superflux()

        self.odf_im = np.repeat(self.superflux_downsampled(),

                           self.s_db.shape[0],

                           axis=0)
        
        return self.odf_im

    def create_image_stack(self):

        return np.dstack((self.create_melspectrogram(),self.create_superflux_image()))
    

        
        