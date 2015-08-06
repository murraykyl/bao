import math
from scipy import integrate
import numpy as np

omega = {"K0":0,
         "M0":0.3183,
         "R0":0,
         "L0":0.6817}

c = 3e5
h = 0.6704
H0 = 100*h
Dh = 3000/h

def hubbleRatio(z):
    """This is an example of a function."""
    return math.sqrt(omega["K0"] * (1+z)**2 + 
                     omega["M0"] * (1+z)**3 + 
                     omega["R0"] * (1+z)**4 + 
                     omega["L0"])

def comovingDistance(z):
    return (integrate.quad(lambda x: 1./hubbleRatio(x),
                           0, z)[0]/H0) * c

def angularDistance(z):
    return comovingDistance(z)/((1+z)*H0)

def luminosityDistance(z):
    return comovingDistance(z)*(1+z)

def comovingAngularDiameterDistance(z):
    return (c/H0) * comovingDistance(z)

def binNumber(nBins, lo, hi, val):
    '''Returns bin number of val for linearly denominated axis.'''
    return int( (nBins - 1) * (val - lo) / (hi - lo))

class ComovingDistance(object):
    """Lookup table for comoving distance"""
    
    def __init__(self, lo, hi, nPoints = 1000):
        self.lookup = [(z, comovingDistance(z))
                       for z in np.arange(lo, hi, (hi-lo)/(nPoints-1))]
        self.lookup.append((hi, comovingDistance(hi)))

    def __call__(self, z):
        lo = self.lookup[0][0]
        hi = self.lookup[-1][0]
        i = binNumber(len(self.lookup), lo, hi, z)
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

def absoluteDistance(xd,yd,zd):                 #Define Distances between Galaxies
    return math.sqrt(xd**2 + yd**2 + zd**2)

def correlationHistogram(histDD, histRR):
    histEp = histDD.Clone("histEp")
    histEp.Reset()
    histEp.Add(histDD, 1)
#    histEp.Add(histRR, 1)
 #   histEp.Add(histDR, -2)
    histEp.Divide(histRR)
    return histEp

