from astropy.io import fits
from astropy.table import Table, vstack
import numpy as np
import correlation
import ROOT as r 
import random


def openTable(filename):
    data = fits.getdata(filename, 1)
    table = Table(data)
    return table

def resize(table):
    table.remove_column('weight_noz')
    table.remove_column('weight_cp')
    table.remove_column('weight_sdc')
    table.remove_column('run')
    table.remove_column('rerun')
    table.remove_column('camcol')
    table.remove_column('field')
    table.remove_column('obj')
    table.remove_column('plate')
    table.remove_column('MJD')
    table.remove_column('fiberID')
    return table
                       
def cuts(table, ras = None, rae = None, decs = None, dece = None):
    table1 = table[np.where(table['ra'] > ras)]
    table2 = table1[np.where(table1['ra'] < rae)]
    table3 = table2[np.where(table2['dec'] > decs)]
    table4 = table3[np.where(table3['dec'] < dece)]
    return table4

def correlationHistogram(histDD, histDpR, histRR):
    histEp = histDD.Clone("histEp")
    histEp.Reset()
    histEp.Add(histDD, 3)
    histEp.Add(histRR, 3)
    histEp.Add(histDpR, -2)
    histEp.Divide(histRR)
    return histEp

def renameData(table):
    return [correlation.cartesian(row) for row in table]

if __name__=="__main__":
    td1 = cuts(resize(openTable('galaxies_DR9_CMASS_North.fits')), 205, 207, 0, 2)
    tr1 = cuts(openTable('randoms_DR9_CMASS_North.fits'), 205, 207, 0, 2)
    tdpr1 = vstack([td1, tr1])
    td = renameData(td1)
    tdpr = renameData(tdpr1)
    tr = renameData(tr1)
    print "Concat"
    print len(td)
    print len(tr)
    print len(tdpr)
    histDD = correlation.histBB(td)
    histDpR = correlation.histBB(tdpr)
    histRR = correlation.histBB(tr)
    print "correlation done"
    histD = histDD.Clone("histD")
    histD.Reset()
    histD.Add(histDD)
    histDR = histDD.Clone("histD")
    histDR.Reset()
    histDR.Add(histDpR)
    histR = histDD.Clone("histD")
    histR.Reset()
    histR.Add(histRR)

    corrhist = correlationHistogram(histD, histDR, histR)

    c = r.TCanvas()
    outFileName = "TestCorrelationFunction.pdf"
    c.Print(outFileName + "[")
    corrhist.Draw()
    c.Print(outFileName)
    histDD.Draw()
    c.Print(outFileName)
    histRR.Draw()
    c.Print(outFileName)
    histDpR.Draw()
    c.Print(outFileName)
    c.Print(outFileName + "]")
