#!/usr/bin/env python

import ROOT as r
import correlation
import argparse
import random

parser = argparse.ArgumentParser(description='Set values')
parser.add_argument('-i', '--input', type=int, help='nstart number', required=True)
parser.add_argument('-o', '--output', type=int, help='nend number', required=True)
args = parser.parse_args() 

def correlationHistogram(histDD, histDpR, histRR):
    histEp = histDD.Clone("histEp")
    histEp.Reset()
    histEp.Add(histDD, 3)
    histEp.Add(histRR, 3)
    histEp.Add(histDpR, -2)
    histEp.Divide(histRR)
    return histEp

if __name__=="__main__":
    nstart = args.input
    nend = args.output
    dataDDn = correlation.openData('data/galaxies_DR9_CMASS_North.fits', nstart, nend)
    dataRRn = correlation.openData('data/randoms_DR9_CMASS_North.fits', nstart, nend)
#    dataDDs = correlation.openData('../Downloads/galaxies_DR9_CMASS_South.fits', npoints)
#    dataRRs = correlation.openData('../Downloads/randoms_DR9_CMASS_South.fits', npoints)
    print "Concat Now"
    DpRn = dataDDn + dataRRn
#    DpRs = dataDDs + dataRRs
    print "First hist"
    histDD1 = correlation.histBB(dataDDn)
    histDpR1 = correlation.histBB(DpRn)
    histRR1 = correlation.histBB(dataRRn)

    histDD = histDD1.Clone("histDDn")
    histDD.Reset()
    histDD.Add(histDD1)
    histDpR = histDD1.Clone("histDDn")
    histDpR.Reset()
    histDpR.Add(histDpR1)
    histRR = histDD1.Clone("histDDn")
    histRR.Reset()
    histRR.Add(histRR1)

    corrHistb = correlationHistogram(histDD, histDpR, histRR)
#    corrHista = correlationHistogram(histDDna, histDpRna, histRRna)

    c = r.TCanvas()
    outFileName = "CorrelationFunction%s.pdf" %random.random()
    c.Print(outFileName + "[")
    corrHistb.Draw()
    c.Print(outFileName)
    histDD.Draw()
    c.Print(outFileName)
    histRR.Draw()
    c.Print(outFileName)
    histDpR.Draw()
    c.Print(outFileName)
    c.Print(outFileName + "]")

#    outFileName = "Correlation FunctionA.pdf"
#    c.Print(outFileName + "[")
#    corrHista.Draw()
#    c.Print(outFileName)
#    histDDna.Draw()
#    c.Print(outFileName)
#    histRRna.Draw()
#    c.Print(outFileName)
#    histDpRna.Draw()
#    c.Print(outFileName)
#    c.Print(outFileName + "]")
#    print corrHistb.GetBinContent(corrHistb.GetNbinsX()+1)
#    print corrHista.GetBinContent(corrHista.GetNbinsX()+1)

#    outFileName = "Corr Func Tri.pdf"
#    c.Print(outFileName + "[")
#    histDRtop.Draw()
#    c.Print(outFileName)
#    histDRbot.Draw()
#    c.Print(outFileName)
#    c.Print(outFileName + "]")
    
