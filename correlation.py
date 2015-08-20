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
parser.add_argument('dataA', metavar='a', type=str, help='Dataset A')
parser.add_argument('dataB', metavar='b', type=str, help='Dataset B')
parser.add_argument('grid1', metavar='i', type=tuple, help='Grid cell a')
parser.add_argument('grid2', metavar='k', type=tuple, help='Grid cell b')
parser.add_argument('njobs', metavar='n', type=int, help='Number of sub jobs')
parser.add_argument('jobID', metavar='m', type=int, help='Job name')
args = parser.parse_args()


def histAB(list1, list2, str):
    hist1 = r.TH1D(str, str+";Mpc;Counts", 200, 0, 200)
    for i in list1:
        for j in list2:
            d = common.absoluteDistance(i[0]-j[0], i[1]-j[1], i[2]-j[2])
            hist1.Fill(d)
    return hist1

def histBB(tab, str):
    hist = r.TH1D(str, "Counts;Mpc;"+str, 200, 0, 200)
    bb = np.array(tab)
    for i,row in enumerate(bb):
        if i%500==0: print "i= ", i
        cc = (row - bb[i+1:]).T[:3].T
        for d in np.sqrt(np.diag(cc.dot(cc.T))):
            hist.Fill(d)
    return hist


if __name__=="__main__":                       

    if args.dataA=="D":
        filename = 'data/galaxies_DR9_CMASS_North.fits'
    else:
        filename = 'data/randoms_DR9_CMASS_North.fits'

    if args.dataB=="D":
        filename1 = 'data/galaxies_DR9_CMASS_North.fits'
    else:
        filename1 = 'data/randoms_DR9_CMASS_North.fits'

    alpha = args.grid1
    beta = args.grid2

    float = "%f" % random.random()
    out1 = "DDHists/"
    out2 = "RRHists/"
    out3 = "DRHists/"
    out4 = "EpHists/"

    if args.dataA==args.dataB && alpha==beta:
        dat = generate.open Data(filename, None, None, grid = (4,4))[alpha[0]][alpha[1]]
        return histAA = histBB(dat, args.dataA+args.dataA+float)
    else:
        dat = generate.openData(filename, None, None, grid = (4, 4))[alpha[0]][alpha[1]]
        dat1 = generate.openData(filename1, None, None, grid = (4, 4))[beta[0]][beta[1]]
        return histAB = histAB(dat, dat1, args.dataA+args.dataB+float)

    for a in Aalph:
        for b in Bbeta:
            hist.Fill(dist(a,b))
        return hist

    for iA in [0,1,2]:
        a = Aalph[iA]
        for b in Bbeta:
            hist.Fill(dist(a,b))
        return hist

    for a in Aalph[args.jobID::(len(Aalph)/args.njobs)]:
        return yes

    for iA,a in enumerate(Aalph):
        for jA in range(iA+1, len(Aalph)):
            hist.Fill(dist(a, Aalph[iA]))
        return hist
                      
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
