"""
    h5files functions
"""
import h5py
import numpy as np

def load_h5(filename):
    """
    Loads an h5 file and returns the data.
    """
    num_imf = 15
    with h5py.File(filename, 'r') as file:
        audio_list = list(file.keys())
        array_data = np.zeros((len(audio_list),num_imf,0))
        for i,audio in enumerate(audio_list):
            array_data[i] = np.array(file[audio])          
    return array_data