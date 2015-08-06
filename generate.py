#!/usr/bin/env python

import random
import numpy as np
import math
from astropy.io import fits
from astropy.table import Table
from scipy import integrate
import common
import itertools

def openTab(filename):
    data = fits.getdata(filename, 1)
    table = Table(data)
    return [common.cartesian(row) for row in table]

def splitTable(tab, list):
    r1 = random.sample(list, len(list)/3)
    r2 = random.sample(tab, len(list)/3)
    r2prime = [common.cartesian(row) for row in r2]
    r3 = random.sample(list, len(list)/3)
    return r1, r2, r3, r2prime

def randomChoose(tab, nPoints = 1000):            
    list = []
    subset = random.sample(tab, nPoints)
    for row in subset:
        w = common.cartesian(row)
        list.append(w)
    return list

def averageNumber(list, tup):
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

def combineLists(list_of_lists):
    listNotMerged = list_of_lists
    merged = list(itertools.chain.from_iterable(listNotMerged))
    return merged
                  

if __name__=='__main__':
    data = fits.getdata('data/randoms_DR9_CMASS_North.fits', 1)
    table = Table(data)
    print "Open Table"
    split = splitTable(table, openTab('data/randoms_DR9_CMASS_North.fits'))
    ran = randomChoose(split[1], 10)
    print ran
    print split[3]
#    slist = []
#    for tup in ran:
 #       ave = averageNumber(split[0], tup)
  #      slist.append(ave)
   # E = slist + [split[0]]
    #print combineLists(E)
