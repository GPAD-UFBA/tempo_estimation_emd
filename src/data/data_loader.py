"""
    Load the data needed for the training.

"""

import sys
import librosa
from src.config.definitions import ROOT_DIR


def audio_loader(file_path):
    """
    Loads the audio from the file_path and returns the data and the sample rate.
    """
    sys.path.append(ROOT_DIR)
    data, sample_rate = librosa.load(ROOT_DIR + file_path)
    return data, sample_rate
