import math
import ROOT as r
import random
import numpy as np
from astropy.io import fits
from astropy.table import Table
import itertools
import common

def histAA(tab):                                #Create Galaxy Pair Histogram
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 100, 0, 200)
    for i,(xi,yi,zi) in enumerate(tab):
        if i%100==0: print "i =", i
        for xj,yj,zj in tab[i+1:]:
            d = common.absoluteDistance(xi-xj, yi-yj, zi-zj)
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
        return [common.cartesian(row) for row in table[nstart:nend]]
    mindec = math.floor(np.min(table['dec']))
    maxdec = math.ceil(np.max(table['dec']))
    minra = math.floor(np.min(table['ra']))
    maxra = math.ceil(np.max(table['ra']))
    print (mindec, maxdec), (minra, maxra)
    triplets = [[[] for j in range(grid[1])] for i in range(grid[0])]
    for row in table:
        i = common.binNumber(grid[0], mindec, maxdec, row['dec'])
        j = common.binNumber(grid[1], minra, maxra, row['ra'])
        triplets[i][j].append(common.cartesian(row) + (row['ra'], row['dec']))
    return triplets
        

if __name__=="__main__":                        #Test Functions
    print common.hubbleRatio(.5)
    print common.absoluteDistance(12-7, 7-3, 9+17)

    openData('data/galaxies_DR9_CMASS_North.fits', grid = (6,20))
    
