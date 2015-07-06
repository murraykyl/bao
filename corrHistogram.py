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
    dataDDnf = correlation.openDataFront('data/galaxies_DR9_CMASS_North.fits', nstart, nend)
    dataRRnf = correlation.openDataFront('data/randoms_DR9_CMASS_North.fits', nstart, nend)
    dataDDnb = correlation.openDataBack('data/galaxies_DR9_CMASS_North.fits', nstart, nend)
    dataRRnb = correlation.openDataBack('data/randoms_DR9_CMASS_North.fits', nstart, nend)
#    dataDDs = correlation.openData('../Downloads/galaxies_DR9_CMASS_South.fits', npoints)
#    dataRRs = correlation.openData('../Downloads/randoms_DR9_CMASS_South.fits', npoints)
    print "Concat Now"
    DpRnf = dataDDnf + dataRRnf
    DpRnb = dataDDnb + dataRRnb
#    DpRs = dataDDs + dataRRs
    print "First hist"
    histDDnf = correlation.histBB(dataDDnf)
    histDpRnf = correlation.histBB(DpRnf)
    histRRnf = correlation.histBB(dataRRnf)
    histDDnb = correlation.histBB(dataDDnb)
    histDpRnb = correlation.histBB(DpRnb)
    histRRnb = correlation.histBB(dataRRnb)

    histDDn = histDDnf.Clone("histDDn")
    histDDn.Reset()
    histDDn.Add(histDDnf)
    histDDn.Add(histDDnb)
    histDpRn = histDDnf.Clone("histDDn")
    histDpRn.Reset()
    histDpRn.Add(histDpRnf)
    histDpRn.Add(histDpRnb)
    histRRn = histDDnf.Clone("histDDn")
    histRRn.Reset()
    histRRn.Add(histRRnf)
    histRRn.Add(histRRnb)

    corrHistb = correlationHistogram(histDDn, histDpRn, histRRn)
#    corrHista = correlationHistogram(histDDna, histDpRna, histRRna)

    c = r.TCanvas()
    outFileName = "CorrelationFunction%s.pdf" %random.random()
    c.Print(outFileName + "[")
    corrHistb.Draw()
    c.Print(outFileName)
    histDDnb.Draw()
    c.Print(outFileName)
    histRRnb.Draw()
    c.Print(outFileName)
    histDpRnb.Draw()
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
    
