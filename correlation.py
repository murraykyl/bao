#!/usr/bin/env python

import math
import ROOT as r
import random
import numpy as np
from astropy.io import fits
from astropy.table import Table
import itertools
import common
import generate

def histAA(list):                                #Create Galaxy Pair Histogram
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 100, 0, 200)
    for (xi,yi,zi) in list:
        if i%100==0: print "i =", i
        for xj,yj,zj in tab[i+1:]:
            d = common.absoluteDistance(xi-xj, yi-yj, zi-zj)
            hist.Fill(d)            
    return hist

def histBB(tab):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 200, 0, 200)
    bb = np.array(tab)
    for i,row in enumerate(bb):
        if i%500==0: print "i= ", i
        cc = (row - bb[i:]).T[:3].T
        for d in np.sqrt(np.diag(cc.dot(cc.T))):
            hist.Fill(d)
    return hist


if __name__=="__main__":                       

#    data = fits.getdata('data/randoms_DR9_CMASS_North.fits', 1)
 #   tabl = Table(data)
  #  print "Open Table"
   # split = generate.splitTable(tabl, generate.openTab('data/randoms_DR9_CMASS_North.fits'))
#    rando = generate.randomChoose(split[1], 10)
 #   print rando
  #  slist = []
   # for tup in rando:
#        ave = generate.averageNumber(split[3], tup)
 #       slist.append(ave)
  #  dataF = random.sample(generate.combineLists(slist + [split[0]]), 2000)
   # dataR = random.sample(split[2], 4000)
    #dataS = random.sample(split[3], 2000)
    #outdir = "output/"

    grid = (6, 20)
    dat = random.sample(generate.openData('data/galaxies_DR9_CMASS_North.fits', None, None, grid = (6, 20))[3][4], 2000)
    histDD = histBB(dat)
    rand = random.sample(generate.openData('data/randoms_DR9_CMASS_North.fits', None, None, grid = (6, 20))[3][4], 4000)
    histRR = histBB(rand)
#    histDpR = histBB(dat+rand)
 #   histDR = histDpR.Clone()
  #  histDR.Add(histDD, -1)
   # histDR.Add(histRR, -1)
    for h in [histDD, histRR]: h.Scale(1./h.Integral())
    histEp = common.correlationHistogram(histDD, histRR)    

    tfile = r.TFile.Open("CorrelationFunctionHistograms.root", "recreate")
    histDD.Write()
    histRR.Write()
 #   histDpR.Write()
    histEp.Write()
    tfile.Close()

    c = r.TCanvas()
    histRR.SetLineColor(r.kRed)
#    histDR.SetLineColor(r.kBlue)
    histEp.SetLineColor(r.kGreen)
    histDD.Draw()
    histRR.Draw("same")
    c.Print("CorrelationHistogramDDRR.pdf")
    histEp.Draw()
    c.Print("CorrelationHistogramDDTot.pdf")



