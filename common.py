

def binNumber(nBins, lo, hi, val):
    '''Returns bin number of val for linearly denominated axis.'''
    return int( (nBins - 1) * (val - lo) / (hi - lo))
