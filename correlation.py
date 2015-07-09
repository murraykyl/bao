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
    hist = r.TH1D("%f"%random.random(), " ;Mpc;d^2Eta(d)", 200, 0, 1000)
    bb = np.array(tab)
    for i,row in enumerate(bb):
        if i%500==0: print "i= ", i
        cc = (row - bb[i:]).T[:3].T
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
    quints = [[[] for j in range(grid[1])] for i in range(grid[0])]
    for row in table:
        i = common.binNumber(grid[0], mindec, maxdec, row['dec'])
        j = common.binNumber(grid[1], minra, maxra, row['ra'])
        quints[i][j].append(common.cartesian(row) + (row['ra'], row['dec']))
    return quints
        
def cellPlotting(quints):
    hist = r.TH2D("%f"%random.random(), " ;RA;Dec", 100, 108, 264, 100, -4, 57)
    M = quints
    for k in range(len(M)):
        hist.Fill(M[k][3], M[k][4])
    return hist


if __name__=="__main__":                       

    outdir = "output/"

    grid = (4, 5)
    dat = openData('data/galaxies_DR9_CMASS_North.fits', grid = (4, 5))[3][3]
    histDD = histBB(dat)
    rand = openData('data/randoms_DR9_CMASS_North.fits', grid = (4, 5))[3][3][::10]
    histRR = histBB(rand)
    histDpR = histBB(dat+rand)
    histDR = histDpR.Clone()
    histDR.Add(histDD, -1)
    histDR.Add(histRR, -1)
    for h in [histDD, histRR, histDR]: h.Scale(1./h.Integral())
    histEp = common.correlationHistogram(histDD, histDR, histRR)    

    tfile = r.TFile.Open("CorrelationFunctionHistograms.root")
    histDD.Write()
    histRR.Write()
    histDpR.Write()
    histEp.Write()
    tfile.Close()

    c = r.TCanvas()
    histRR.SetLineColor(r.kRed)
    histDR.SetLineColor(r.kBlue)
    histEp.SetLineColor(r.kGreen)
    histDD.Draw()
    histRR.Draw("same")
    histDpR.Draw("same")
    c.Print("CorrelationHistogramDatRan.pdf")
    histEp.Draw()
    c.Print("CorrelationHistogramTotal.pdf")
    histDD.Divide(histRR)
    histDD.Draw()
    c.Print("CorrelationDDRR.pdf")
