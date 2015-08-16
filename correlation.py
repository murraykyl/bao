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

def histAA(list, str):
    hist = r.TH1D(str, str+";Mpc;d^2Eta(d)", 100, 0, 200)
    for (xi,yi,zi) in list:
        if i%100==0: print "i =", i
        for xj,yj,zj in tab[i+1:]:
            d = common.absoluteDistance(xi-xj, yi-yj, zi-zj)
            hist.Fill(d)            
    return hist

def histBB(tab, str):
    hist = r.TH1D(str, str+";Mpc;d^2Eta(d)", 200, 0, 200)
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
    #rando = generate.randomChoose(split[1], 1)
#    print rando
 #   slist = []
  #  for tup in rando:
   #     ave = generate.averageNumber(split[3], tup)
    #    slist.append(ave)
#    dataF = random.sample(generate.combineLists(slist + [split[0]]), 3000)
 #   dataR = random.sample(split[2], 6000)
  #  dataS = random.sample(split[3], 2000)
   # outdir = "output/"

    float = "%f" % random.random()
    grid = (4, 5)
    dat = random.sample(generate.openData('data/galaxies_DR9_CMASS_North.fits', 
                                          None, None, grid = (4, 5))[1][1], 3000)
    histDD = histBB(dat, "DD"+float)
    rand = random.sample(generate.openData('data/randoms_DR9_CMASS_North.fits', 
                                           None, None, grid = (4, 5))[1][1], 7000)
    histRR = histBB(rand, "RR"+float)
    histDpR = histBB(dat+rand, "DR"+float)
    histDR = histDpR.Clone()
    histDR.Add(histDD, -1)
    histDR.Add(histRR, -1)
    for h in [histDD, histDR, histRR]: h.Scale(1./h.Integral())
    histEp = common.correlationHistogram(histDD, histDR, histRR)    

#    tfile = r.TFile.Open("IndHists"+float+".root", "recreate")
 #   histDD.Write()
  #  histRR.Write()
   # histDR.Write()
    #tfile.Close()

    tfile2 = r.TFile.Open("EpHist"+float+".root", "recreate")
    histEp.Write()
    tfile2.Close()

#    c = r.TCanvas()
#    histRR.SetLineColor(r.kRed)
 #   histDR.SetLineColor(r.kBlue)
  #  histDD.Draw()
   # c.Print("DDHist%r"%random.random())
    #histDR.Draw()
#    c.Print("DRHist%f"%random.random())
 #   histRR.Draw()
  #  c.Print("RRHist%d"%random.random())
 #   histEp.Draw()
  #  c.Print("EpHist"+float+".pdf")



