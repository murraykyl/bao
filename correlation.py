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
import argparse

parser = argparse.ArgumentParser(description='Grid values.')
parser.add_argument('gridi', metavar='i', type=int, help='The ith value of gridding')
parser.add_argument('gridj', metavar='j', type=int, help='The jth value of gridding')
parser.add_argument('nstart', metavar='n', type=int, help='Beginning of cut')
parser.add_argument('nend', metavar='e', type=int, help='End of cut')
args = parser.parse_args()

def histBB(tab, str):
    hist = r.TH1D(str, "Counts;Mpc;"+str, 200, 0, 200)
    bb = np.array(tab)
    for i,row in enumerate(bb):
        if i%500==0: print "i= ", i
        cc = (row - bb[i+1:]).T[:3].T
        for d in np.sqrt(np.diag(cc.dot(cc.T))):
            hist.Fill(d)
    return hist

def histAB(list1, list2, str):
    hist1 = r.TH1D(str, str+";Mpc;"+str, 200, 0, 200)
    for i in list1:
        for j in list2:
            d = common.absoluteDistance(i[0]-j[0], i[1]-j[1], i[2]-j[2])
            hist1.Fill(d)
    return hist1

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
    out1 = "DDHists/"
    out2 = "RRHists/"
    out3 = "DRHists/"
    out4 = "EpHists/"
    nstart = args.nstart
    nend = args.nend
    grid = (4, 4)
    dat = generate.openData('data/galaxies_DR9_CMASS_North.fits', 
                            None, None, 
                            grid = (4, 4))[args.gridi][args.gridj][nstart:nend]
#    dat1 = generate.openData('data/galaxies_DR9_CMASS_North.fits', 
 #                           None, None, 
  #                          grid = (4, 4))[(args.gridi+1)%4==0][args.gridj][nstart:nend]
    histDD = histBB(dat, "DD"+float)
   # histDDD = histAB(dat, dat1, "DDD"+float)
    rand = generate.openData('data/randoms_DR9_CMASS_North.fits', 
                             None, None, 
                             grid = (4, 4))[args.gridi][args.gridj][nstart:2*nend]
    histRR = histBB(rand, "RR"+float)
    histDpR = histBB(dat+rand, "DR"+float)
    histDR = histDpR.Clone()
    histDR.Add(histDD, -1)
    histDR.Add(histRR, -1)
    histEp = common.correlationHistogram(histDD, histDR, histRR)

    DDhist = histDD.Clone("DDhist")
    RRhist = histRR.Clone("RRhist")
    DRhist = histDR.Clone("DRhist")

    tfile = r.TFile.Open(out1+"DDHist"+float+".root", "recreate")
    DDhist.Write()
    tfile.Close()

    tfile2 = r.TFile.Open(out2+"RRHist"+float+".root", "recreate")
    RRhist.Write()
    tfile2.Close()

    tfile3 = r.TFile.Open(out3+"DRHist"+float+".root", "recreate")
    DRhist.Write()
    tfile3.Close()

    tfile4 = r.TFile.Open("EpHist"+float+".root", "recreate")
    histEp.Write()
    tfile4.Close()

 #   tfile5 = r.TFile.Open("DDDhist"+float+".root", "recreate")
  #  histDDD.Write()
   # tfile5.Close()
