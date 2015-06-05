import math
from scipy import integrate
import numpy as np

omega = {"K0":0,
         "M0":0.33,
         "R0":0,
         "L0":0.67}

def hubbleRatio(z):
    """This is an example of a function."""
    return math.sqrt(omega["K0"] * (1+z)**2 + 
                     omega["M0"] * (1+z)**3 + 
                     omega["R0"] * (1+z)**4 + 
                     omega["L0"])

def comovingDistance(z):
    return integrate.quad(lambda x: 1./hubbleRatio(x),
                          0, z)[0]

def angularDistance(z):
    return comovingDistance(z)/(1+z)

def luminosityDistance(z):
    return comovingDistance(z)*(1+z)

class ComovingDistance(object):
    """Lookup table for comoving distance"""
    
    def __init__(self, lo, hi, nPoints = 1000):
        self.lookup = [(z, comovingDistance(z))
                       for z in np.arange(lo, hi, (hi-lo)/(nPoints-1))]
        self.lookup.append((hi, comovingDistance(hi)))

    def __call__(self, z):
        lo = self.lookup[0][0]
        hi = self.lookup[-1][0]
        i = int( (len(self.lookup)-1) * (z - lo) / (hi - lo))
        x0,y0 = self.lookup[i]
        x1,y1 = self.lookup[i+1]
        return y0 + (z - x0) * (y1 - y0) / (x1 - x0)
                              
if __name__=="__main__":
    assert 1 == sum(omega.values())
    assert comovingDistance(0) == 0
    assert hubbleRatio(0) == 1

    from random import uniform

    cd = ComovingDistance(0.4, 0.7)
    for i in range(100):
        z = uniform(0.4, 0.7)
        a = comovingDistance(z)
        b = cd(z)
        assert abs(a-b) < 1e-6
