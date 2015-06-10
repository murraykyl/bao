from astropy.io import fits
from astropy.table import Table
import ROOT as r
import numpy as np
import correlation

r.gROOT.SetBatch(1)

def correlationHistogram(histDD, histDpR, histRR):
    histEp = histDD.Clone("histEp")
    histEp.Reset()
    histEp.Add(histDD, 3)
    histEp.Add(histRR, 3)
    histEp.Add(histDpR, -2)
    histEp.Divide(histRR)
    return histEp

if __name__=="__main__":
    print "Open Table 1"
    dataDD = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)   #DD
    tDD = Table(dataDD)
    print "Open Table 2"
    dataRR = fits.getdata('../Downloads/randoms_DR9_CMASS_North.fits', 1)    #RR
    tRR = Table(dataRR)
    print "Delete Columns"
    del tDD['weight_noz']
    del tDD['weight_cp']
    del tDD['weight_sdc']
    del tDD['run']
    del tDD['rerun']
    del tDD['camcol']
    del tDD['field']
    del tDD['obj']
    del tDD['plate']
    del tDD['MJD']
    del tDD['fiberID']
    tDD.rename_column('weight_fkp', 'weight')
    print "Concat Now"
    tDpR = np.concatenate((tDD.as_array(),tRR.as_array()), axis=0)              #D+R
    print "First hist"
    histDD = correlation.histAA(tDD)
    histDpR = correlation.histAA(tDpR)
    histRR = correlation.histAA(tRR)
    corrHist = correlationHistogram(histDD, histDpR, histRR)
    c = r.TCanvas()
    corrHist.Draw()
    c.Print("Correlation Function.pdf")
    print corrHist.GetBinContent(corrHist.GetNbinsX()+1)
