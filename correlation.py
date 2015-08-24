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
parser.add_argument('grid1i', metavar='i', type=int, help='The ith component of cell a')
parser.add_argument('grid1j', metavar='j', type=int, help='The jth component of cell a')
parser.add_argument('grid2i', metavar='k', type=int, help='The ith component of cell b')
parser.add_argument('grid2j', metavar='l', type=int, help='The ith component of cell b')
parser.add_argument('njobs', metavar='n', type=int, help='Number of jobs for cell')
parser.add_argument('jobID', metavar='m', type=int, help='Job ID number')
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

def resultHist(file, file1, dataA, dataB, gridA, gridB, str):
    if dataA==dataB and gridA==gridB:
        dat = generate.openData(filename, None, None, grid = (4,4))[gridA[0]][gridA[1]]
        print (len(dat)*(len(dat)-1))/2
        hist = histBB(dat, dataA+dataB+str)
    else:
        Aalpha = generate.openData(file, None, None, grid = (4,4))[gridA[0]][gridA[1]]
        Bbeta = generate.openData(file1, None, None, grid = (4,4))[gridB[0]][gridB[1]]
        print len(Aalpha)*len(Bbeta)
        hist = histAB(Aalpha, Bbeta, dataA+dataB+str)
    return hist                      


if __name__=="__main__":                       

    if args.dataA=="D":
        filename = 'data/galaxies_DR9_CMASS_North.fits'
    elif args.dataA=="R":
        filename = 'data/randoms_DR9_CMASS_North.fits'
    elif args.dataA=="Sg":
        filename = 'data/sampleg_DR9_CMASS_North.fits'
    else:
        filename = 'data/sampler_DR9_CMASS_North.fits'

    if args.dataB=="D":
        filename1 = 'data/galaxies_DR9_CMASS_North.fits'
    elif args.dataB=="R":
        filename1 = 'data/randoms_DR9_CMASS_North.fits'
    elif args.dataB=="Sg":
        filename1 = 'data/sampleg_DR9_CMASS_North.fits'
    else:
        filename1 = 'data/sampler_DR9_CMASS_North.fits'

    alpha = (args.grid1i, args.grid1j)
    beta = (args.grid2i, args.grid2j)

    njobs = args.njobs
    jobID = args.jobID

    float = "%f" % random.random()
    print float

    hist = resultHist(filename, filename1, args.dataA, args.dataB, alpha, beta, float)

#    if dataA==dataB and alpha==beta:
 #       for iA,a in enumerate(Aalpha):
  #          for jA in range(iA+1, len(Aalpha)):
   #             hist.Fill(common.absoluteDistance(a[0]-Aalpha[jA][0], 
    #                                              a[1]-Aalpha[jA][1], 
     #                                             a[2]-Aalpha[jA][2]))
#    elif dataA==dataB and alpha==beta:
 #       for a in Aalph[jobID::(len(Aalpha)/njobs)]:
  #          for ja in Aalpha[jobID::(len(Aalpha)/njobs)]:
   #             hist.Fill(a[0]-ja[0], a[1]-ja[1], a[2]-ja[2])
#    elif len(Aalpha)<10000:
 #       for a in Aalpha:
  #          for b in Bbeta:
   #             hist.Fill(common.absoluteDistance(a[0]-b[0], a[1]-b[1], a[2]-b[2]))
#    elif len(Aalpha)<10000:
 #       for iA in [0,1,2]:
  #          a = Aalph[iA]
   #         for b in Bbeta:
    #            hist.Fill(dist(a[0]-b[0], a[1]-b[1], a[2]-b[2]))
#    else:
 #       pass
                      
    DDhist = hist.Clone("DDhist")

    print DDhist

    tfile = r.TFile.Open("DDHist"+float+".root", 
                         "recreate")
    DDhist.Write()
    tfile.Close()


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
