"""
    Prerocessing functions
"""
import numpy as np
from src.features.onset_detector import OnsetDetector
from src.features.periodicity_detection import periodicity_detection


def preprocess_data(array):
    """
    Preprocesses the imf data to detecting onsets and periodicity.
    """
    onset_detector = OnsetDetector()
    sr = 11025
    num_imf = 15
    pedf_array = np.zeros((len(array),num_imf,0))   
    for index, audio in enumerate(array):
        for imf_index, imf in enumerate(audio):
            pedf_array[index][imf_index] = periodicity_detection(onset_detector.odf(imf,sr))

    return pedf_array
