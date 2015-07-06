import math
from scipy import integrate
import ROOT as r
import random
import numpy as np
from astropy.io import fits
from astropy.table import Table
import itertools
import common

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

def absoluteDistance(xd,yd,zd):                 #Define Distances between Galaxies
    return math.sqrt(xd**2 + yd**2 + zd**2)



def histAA(tab):                                #Create Galaxy Pair Histogram
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 100, 0, 200)
    for i,(xi,yi,zi) in enumerate(tab):
        if i%100==0: print "i =", i
        for xj,yj,zj in tab[i+1:]:
            d = absoluteDistance(xi-xj, yi-yj, zi-zj)
            hist.Fill(d)            
    return hist

def histBB(tab):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 100, 0, 1000)
    bb = np.array(tab)
    for i,row in enumerate(bb):
        if i%500==0: print "i= ", i
        cc = row - bb[i:]
        for d in np.sqrt(np.diag(cc.dot(cc.T))):
            hist.Fill(d)            
    return hist

    

def openData(filename, nstart = None, nend = None, grid = None):
    data = fits.getdata(filename, 1)
    table = Table(data)
    print "Open Table ", filename
    if grid == None:
        return [cartesian(row) for row in table[nstart:nend]]
    mindec = math.floor(np.min(table['dec']))
    maxdec = math.ceil(np.max(table['dec']))
    minra = math.floor(np.min(table['ra']))
    maxra = math.ceil(np.max(table['ra']))
    print mindec, maxdec, minra, maxra
    triplets = [[[] for j in range(grid[1])] for i in range(grid[0])]
    for row in table:
        i = common.binNumber(grid[0], mindec, maxdec, row['dec'])
        j = common.binNumber(grid[1], minra, maxra, row['ra'])
        triplets[i][j].append(cartesian(row) + (row['ra'], row['dec']))
    return triplets
        


    





if __name__=="__main__":                        #Test Functions
    print hubbleRatio(.5)
    print distanceMeasure(.6)
    print absoluteDistance(12-7, 7-3, 9+17)

    cd = ComovingDistance(0.4, 0.7)
    for i in range(100):
        w = np.random.uniform(0.4, 0.7)
        a = distanceMeasure(w)
        b = cd(w)
        assert abs(a-b) < 1e-4

    openData('data/galaxies_DR9_CMASS_North.fits', grid = (6,20))
    
