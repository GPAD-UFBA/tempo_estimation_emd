"""
    h5files functions
"""
import h5py
import numpy as np
from src.config.definitions import ROOT_DIR

def load_h5(filename,size=64):
    """
    Loads an h5 file and returns the data.
    """
    with h5py.File(ROOT_DIR +'/'+ filename, 'r') as file:
        audio_list = list(file.keys())
        shape_array = np.array(file[audio_list[0]]).T.shape
        array_data = np.zeros((len(audio_list),*shape_array))
        
        for i,audio in enumerate(audio_list):
            if i < size:
                array_data[i] = np.array(file[audio]).T
                      
    return array_data