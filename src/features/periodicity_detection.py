"""
    Return the periodicity of the odf.
"""

from librosa import autocorrelate

def periodicity_detection(odf):
    """
        Return the periodicity of the odf.
    """
    return autocorrelate(odf)
    