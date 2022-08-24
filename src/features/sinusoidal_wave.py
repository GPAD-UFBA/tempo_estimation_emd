import numpy as np



def sinusoidal_wave(ndata,amplitude,half_period):

    t = np.arange(0, 2*half_period-1)
    f = 0.5/half_period
    yt = np.cos(2*np.pi*f*t)
    yt = amplitude*yt
    nyt = len(yt)
    no = int(np.ceil(ndata/nyt))
    
    
    y = np.tile(yt,(1,no))
    y = y[0:ndata]
    
    return y 
    