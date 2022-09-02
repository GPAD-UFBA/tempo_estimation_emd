"""
    Prerocessing functions
"""
import numpy as np
from src.features.onset_detector import OnsetDetector
from src.features.periodicity_detection import periodicity_detection


def preprocess_data(array,sr = 16_000):
    """
    Preprocesses the imf data to detecting onsets and periodicity.
    """
    onset_detector = OnsetDetector()
    pedf_array = np.zeros((array.shape)) 
    
    

    for imf_index, imf in enumerate(array):
        pedf_array[imf_index] = periodicity_detection(onset_detector.odf(imf,sr))

    return pedf_array
