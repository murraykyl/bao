#!/usr/bin/env python

import random
import numpy as np
import math
from astropy.io import fits
from astropy.table import Table
from scipy import integrate
import common

def openTab(filename):
    data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
    table = Table(data)
    return [common.cartesian(row) for row in table]

def randomChoose(tab, nPoints = 1000):            
    list = []
    for row in tab:
        w = common.cartesian(row)
        list.append(w)
    return random.sample(list, nPoints)

def averageNumber(filename, tab, tuple):
    Ran = [tuple]
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

def localize(list):
    local = []
    x = -list[0][0]
    y = -list[0][1]
    z = -list[0][2]
    for (xi,yi,zi) in list:
        Q = (xi+x,yi+y,zi+z)
        local.append(Q)
    return local

def spherical(list):
    sphere = []
    r = 150
    for xi,yi,zi in list:
        theta = math.acos(zi/r)
        phi = math.acos((xi/r)*math.cos(theta))
        P = (r, theta, phi)
        sphere.append(P)
    return sphere


if __name__=='__main__':
    data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
    table = Table(data)
    print "Open Table"
    Ran = randomChoose(table, 20)
    print Ran
    for tuple in Ran:
        Ave = averageNumber(openTab('data/galaxies_DR9_CMASS_North.fits'), table, tuple)
        print spherical(localize(Ave))
    
