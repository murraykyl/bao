#!/usr/bin/env python

import random
import numpy as np
import math
from astropy.io import fits
from astropy.table import Table
from scipy import integrate
import common

def randomChoose(tab, nPoints = 1000):            
    list = []
    for row in tab:
        w = common.cartesian(row)
        list.append(w)
    return random.sample(list, nPoints)
    
#def circleGal(p = 150):
 #   list = randomChoose(tab, nPoints)
  #  for xi, yi, zi in list:
   #     p**2 = (xn-xi)**2 + (yn-yi)**2 + (zn-zi)**2
    #return xn, yn, zn

def openTab(filename):
    data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
    table = Table(data)
    return [common.cartesian(row) for row in table]

def averageNumber(filename, tab):
    Ran = randomChoose(tab, 1)
    Ave = []
    for xi,yi,zi in Ran:
        for xj,yj,zj in openTab(filename):
            d = common.absoluteDistance(xj-xi, yj-yi, zj-zi)
            if 149 < d < 151:
                Ave.append((xj,yj,zj))
            else:
                pass
    return Ran + Ave

def poissonDist(n, x):
    return ((n**x)*(math.e**(-n)))/math.factorial(x)

def localize():
    pass



if __name__=='__main__':
    data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
    table = Table(data)
    print "Open Table"
    Ave = averageNumber(openTab('data/galaxies_DR9_CMASS_North.fits'), table)
    print Ave


