from astropy.io import fits
from astropy.table import Table
import ROOT as r
import numpy as np
import correlation

r.gROOT.SetBatch(1)

def correlationHistogram(histDDn, histDpRn, histRRn, histDDs, histDpRs, histRRs):
    histDD = histDDn.Clone("histDD")
    histDD.Reset()
    histDD.Add(histDDn)
    histDD.Add(histDDs)
    histDpR = histDDn.Clone("histDD")
    histDpR.Reset()
    histDpR.Add(histDpRn)
    histDpR.Add(histDpRs)
    histRR = histDDn.Clone("histDD")
    histRR.Reset()
    histRR.Add(histRRn)
    histRR.Add(histRRs)
    histEp = histDD.Clone("histEp")
    histEp.Reset()
    histEp.Add(histDD, 3)
    histEp.Add(histRR, 3)
    histEp.Add(histDpR, -2)
    histEp.Divide(histRR)
    return histEp

if __name__=="__main__":
    print "Open Table 1"
    dataDDn = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)   #DDNorth
    tDDn = Table(dataDDn)
    print "Open Table 2"
    dataRRn = fits.getdata('../Downloads/randoms_DR9_CMASS_North.fits', 1)    #RRNorth
    tRRn = Table(dataRRn)
    print "Open Table 3"
    dataDDs = fits.getdata('../Downloads/galaxies_DR9_CMASS_South.fits', 1)   #DDSouth
    tDDs = Table(dataDDs)
    print "Open Table 4"
    dataRRs = fits.getdata('../Downloads/randoms_DR9_CMASS_South.fits', 1)    #RRSouth
    tRRs = Table(dataRRs)
    print "Delete Columns"
    del tDDn['weight_noz']
    del tDDn['weight_cp']
    del tDDn['weight_sdc']
    del tDDn['run']
    del tDDn['rerun']
    del tDDn['camcol']
    del tDDn['field']
    del tDDn['obj']
    del tDDn['plate']
    del tDDn['MJD']
    del tDDn['fiberID']
    tDDn.rename_column('weight_fkp', 'weight')
    del tDDs['weight_noz']
    del tDDs['weight_cp']
    del tDDs['weight_sdc']
    del tDDs['run']
    del tDDs['rerun']
    del tDDs['camcol']
    del tDDs['field']
    del tDDs['obj']
    del tDDs['plate']
    del tDDs['MJD']
    del tDDs['fiberID']
    tDDs.rename_column('weight_fkp', 'weight')
    print "Concat Now"
    tDpRn = np.concatenate((tDDn.as_array(),tRRn.as_array()), axis=0)        #D+RNorth
    tDpRs = np.concatenate((tDDs.as_array(),tRRs.as_array()), axis=0)        #D+RSouth
    print "First hist"
    cd = correlation.ComovingDistance(0.4, 0.7)
    histDDn = correlation.histAA(tDDn)
    histDpRn = correlation.histAA(tDpRn)
    histRRn = correlation.histAA(tRRn)
    histDDs = correlation.histAA(tDDs)
    histDpRs = correlation.histAA(tDpRs)
    histRRs = correlation.histAA(tRRs)
    corrHist = correlationHistogram(histDDn, histDpRn, histRRn, histDDs, histDpRs, histRRs)
    c = r.TCanvas()
    corrHist.Draw()
    c.Print("Correlation Function.pdf")
    print corrHist.GetBinContent(corrHist.GetNbinsX()+1)
