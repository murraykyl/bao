import random
import numpy as np
import math
from astropy.io import fits
from astropy.table import Table
from scipy import integrate
import ROOT as r

c = 3e5     #km/s
h = 0.7     #dimensionless universe scale
H0 = 100*h  #km/s/Mpc
Dh = 3000/h #Mpc
omega = {"K0": 0,  #Curvature
         "M0": .3, #Matter
         "R0": 0,  #Radiation
         "L0": .7} #Cosmological Constant

def hubbleRatio(z):                             #H(z)/H_0
    return math.sqrt(omega["K0"] * (1+z)**2 +
                     omega["M0"] * (1+z)**3 +
                     omega["R0"] * (1+z)**4 +
                     omega["L0"])

def distanceMeasure(z):                         #Comoving Distance Measure
    return (integrate.quad(lambda m: 1/hubbleRatio(m), 
                           0, z)[0] / H0) * c

class ComovingDistance(object):
    """Lookup table for comoving distance"""
    
    def __init__(self, lo, hi, nPoints = 1000):
        self.lookup = [(z, distanceMeasure(z))
                       for z in np.arange(lo, hi, (hi-lo)/(nPoints-1))]
        self.lookup.append((hi, distanceMeasure(hi)))

    def __call__(self, z):
        lo = self.lookup[0][0]
        hi = self.lookup[-1][0]
        i = int((len(self.lookup)-1) * (z - lo) / (hi - lo))
        x0,y0 = self.lookup[i]
        x1,y1 = self.lookup[i+1]
        return y0 + (z - x0) * (y1 - y0) / (x1 - x0)

cd = ComovingDistance(0.43, 0.7)

def cartesian(row):                             #Convert to Cartesian Coordinates
    """Define New Variable and Convert to Cartesian Coordinates"""
    r = cd(row['z'])                            #Comoving Distances
    ra1 = math.pi*row['ra']/180                 #Convert to Radians
    dec1 = math.pi*row['dec']/180               #Convert to Radians
    x = r * math.cos(ra1) * math.cos(dec1)      #X-Coordinate
    y = r * math.sin(ra1) * math.cos(dec1)      #Y-Coordinate
    z = r * math.sin(dec1)                      #Z-Coordinate
    return x,y,z

def ranChoose(tab):
    """Define Random Selection"""
    list = []
    for row in tab:
        w = cartesian(row)
        list.append(w)
    return random.sample(list, 10000)

if __name__=='__main__':
    data = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
    tab = Table(data)

