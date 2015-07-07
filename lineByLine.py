#!/usr/bin/env python

import math
from scipy import integrate
import random
import numpy as np
from astropy.io import fits
from astropy.table import Table
import ROOT as r
import common
import correlation

def lineByLineAB(filename1, filename2, nStart, nEnd):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;Eta(d)", 100, 0, 5000)
    data1 = fits.getdata(filename1, 1)
    data2 = fits.getdata(filename2, 1)
    tab1 = Table(data1)
    tab2 = Table(data2)
    list1 = [common.cartesian(row) for row in tab1]
    list2 = [common.cartesian(row) for row in tab2]
    for i,(xi,yi,zi) in enumerate(list1):
        if i%1==0: print "i= ", i
        if nStart < i < nEnd:
            for xj,yj,zj in list2:
                d = common.absoluteDistance(xi-xj,yi-yj,zi-zj)
                hist.Fill(d)
        else:
            pass
    return hist
    
def lineByLineAA(filename, nStart, nEnd):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;Eta(d)", 100, 0, 5000)
    data = fits.getdata(filename, 1)
    table = Table(data)
    list = [common.cartesian(row) for row in table]
    for i,(xi,yi,zi) in enumerate(list):
        if nStart < i < nEnd: 
            if i%1==0: print "i= ", i
            for xj,yj,zj in list[i+1:]:
                d = common.absoluteDistance(xi-xj, yi-yj, zi-zj)
                hist.Fill(d)
        else:
            pass
    return hist

if __name__=="__main__":

    filename1 = 'data/galaxies_DR9_CMASS_North.fits'
    filename2 = 'data/randoms_DR9_CMASS_North.fits'
    sameFile = filename1 == filename2
    if sameFile:
        lineHist = lineByLineAA(filename1, 0, 10)    
    else:
        doubleHist = lineByLineAB(filename1, filename2, 0, 10)
    
    c = r.TCanvas()
    outFileName = "LineByLine%s.pdf" %random.random()
    if sameFile:
        lineHist.Draw()
    else:
        doubleHist.Draw()
    c.Print(outFileName)




#    for row in t:
 #       ra1 = row['ra']
  #      dec1 = row['dec']
   #     z1 = row['z']
    #    wcp1 = row['weight_cp']
     #   wfkp1 = row['weight_fkp']
      #  wrf1 = row['weight_noz']
       # wsys1 = row['weight_sdc']
        #w1 = wfkp1*wsys1*(wrf1 + wcp1 + 1)
#        for row in t2:
 #           ra2 = row['ra']
  #          dec2 = row['dec']
   #         z2 = row['z']
    #        wcp2 = row['weight_cp']
     #       wfkp2 = row['weight_fkp']
      #      wrf2 = row['weight_noz']
       #     wsys2 = row['weight_sdc']
        #    w2 = wfkp2*wsys2*(wrf2 + wcp2 + 1)
            
       # w = w1*w2
            
