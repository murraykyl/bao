import math
from scipy import integrate
import ROOT as r
import random

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

def cartesian(row):                             #Convert to Cartesian Coordinates
    """Define New Variable and Convert to Cartesian Coordinates"""
    r = distanceMeasure(row['z'])               #Comoving Distances
    ra1 = math.pi*row['ra']/180                 #Convert to Radians
    dec1 = math.pi*row['dec']/180               #Convert to Radians
    x = r * math.cos(ra1) * math.cos(dec1)      #X-Coordinate
    y = r * math.sin(ra1) * math.cos(dec1)      #Y-Coordinate
    z = r * math.sin(dec1)                      #Z-Coordinate
    return x,y,z

def absoluteDistance(xd,yd,zd):                 #Define Distances between Galaxies
    return math.sqrt(xd**2 + yd**2 + zd**2)

def histAA(tab):                                #Create Correlation Function
    hist = r.TH1D("%f"%random.random(), " ;Log 1+Distance;Counts per Bin", 100, 0, 10)
    for i in range(len(tab)):
        print "i =", i
        for j in range(len(tab))[i+1:]:
            xi,yi,zi = cartesian(tab[i])
            xj,yj,zj = cartesian(tab[j])
            d = absoluteDistance(xi-xj, yi-yj, zi-zj)
            hist.Fill(math.log(1+d))            
            if j > 100:
                break
        if i == 100:
            break
    return hist

if __name__=="__main__":                        #Test Functions
    print hubbleRatio(.5)
    print distanceMeasure(.6)
    print absoluteDistance(12-7, 7-3, 9+17)
    
