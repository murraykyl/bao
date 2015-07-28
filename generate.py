#!/usr/bin/env python

import random
import numpy as np
import math
from astropy.io import fits
from astropy.table import Table
from scipy import integrate
import common

def openTab(filename):
    data = fits.getdata(filename, 1)
    table = Table(data)
    return [common.cartesian(row) for row in table]

def randomChoose(tab, nPoints = 1000):            
    subset = []
    list = []
    subset = random.sample(tab, nPoints)
    for row in subset:
        w = common.cartesian(row)
        list.append(w)
    return list

def averageNumber(list, tab, tup):
    ran = [tup]
    ave = []
    for xi,yi,zi in ran:
        for xj,yj,zj in list:
            d = common.absoluteDistance(xj-xi, yj-yi, zj-zi)
            if 149 < d < 151:
                ave.append((xj,yj,zj))
            else:
                pass
    return ran + ave

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
    for xi,yi,zi in list:
        r = math.sqrt(xi**2 + yi**2 + zi**2)
        theta = math.atan(yi/xi)
        phi = math.atan(math.sqrt(xi**2+yi**2)/zi)
        P = (r, theta, phi)
        sphere.append(P)
    return sphere


if __name__=='__main__':
    data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
    table = Table(data)
    print "Open Table"
    ran = randomChoose(table, 20)
    print ran
    for tup in ran:
        ave = averageNumber(openTab('data/galaxies_DR9_CMASS_North.fits'), table, tup)
        print spherical(localize(ave))
    
