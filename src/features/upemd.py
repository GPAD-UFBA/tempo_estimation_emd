import numpy as np
import emd
from sinusoidal_wave import sinusoidal_wave


class UPEMD:
    
    def __init__(self, start_mode:int = 0, num_imf:int=15, num_sift:int=10, max_phase_0:int = 8, amp_sin_0:float = 0.5):
        
        self.start_mode = start_mode
        self.num_imf = num_imf
        self.num_sift = num_sift
        self.max_phase_0 = max_phase_0
        self.amp_sin_0 = amp_sin_0

        self.start_shift = int(0)
        
        self.count_mode = 0
        self.count_shift = 0
        
        self.conf = emd.sift.get_config('sift')
        self.conf['imf_opts']['max_iters'] = self.num_sift
        
        
    
    def set_signal(self,raw_signal):
        self.signal = raw_signal.reshape(1,-1)
        
    def set_n_data(self):
        self.n_data = int(self.signal.shape[1])
        
    def set_max_imf(self):
        default_max_imf = np.floor(np.log2(self.n_data))
        if (self.num_imf > default_max_imf):
            self.num_imf = default_max_imf   

    def set_last_mode(self):
        self.last_mode = int(self.start_mode + self.num_imf)
        
    def validate_parameters(self,raw_signal):
        self.set_signal(raw_signal)
        self.set_n_data()
        self.set_max_imf()
        self.set_last_mode()
    
    def set_num_shift(self,mode):
        self.num_shift = 2**(mode+1)
        
    def set_num_phase(self):
        self.num_phase = 2**(np.floor(np.log2(self.max_phase_0)))

        if (self.num_phase > self.num_shift):
            self.num_phase = np.min([self.num_phase,self.num_shift])
        

    def assert_numshift_numphase(self):
        assert((self.num_shift % self.num_phase) == 0)

    def make_shift(self):
        
        stop_shift = int(self.start_shift + self.num_shift -1)
        for shift in range(self.start_shift, stop_shift, self.ds):
                       
            print(self.media_array[shift:(shift+self.n_data-1)].shape)

            media = self.media_array[0][shift : shift+self.n_data].reshape((1,-1))
            


            self.count_shift += 1
            
            self.y = self.res + media
            self.y = self.y.reshape(-1)
            sub_imf = emd.sift.sift(self.y, **self.conf)
            sub_imf = np.transpose(sub_imf)
            sub_imf[0,:] = sub_imf[0,:] - media
            self.sum_wrk = self.sum_wrk + sub_imf[0,:]
    
    def make_modes(self):
        imf = np.zeros((self.last_mode,self.n_data))
        
        for mode in range(self.start_mode,self.last_mode - 1):
            self.amp_sin = self.amp_sin_0*np.std(self.res)
            
            self.set_num_shift(mode)
            self.set_num_phase()
            
            self.assert_numshift_numphase()
            self.ds = int(self.num_shift/self.num_phase)
            
            self.media_array = sinusoidal_wave(2*self.n_data,self.amp_sin,(self.num_shift/2))
            self.sum_wrk = np.zeros((1,self.n_data))
            
            self.make_shift()
            
            imf[self.count_mode,:] = self.sum_wrk/self.count_shift
            self.res = self.res - imf[self.count_mode,:]
            self.count_mode += 1
        imf[self.count_mode,:] = self.res
    
        return imf.T
        
    def upemd(self,raw_signal):
        self.validate_parameters(raw_signal)
        self.res = self.signal
        return self.make_modes()
    
            
            
            
            
            
            

        


    
    