import ROOT as r
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
    npoints = 1000
    dataDDn = correlation.openData('../Downloads/galaxies_DR9_CMASS_North.fits', npoints)
    dataRRn = correlation.openData('../Downloads/randoms_DR9_CMASS_North.fits', npoints)
#    dataDDs = correlation.openData('../Downloads/galaxies_DR9_CMASS_South.fits', npoints)
#    dataRRs = correlation.openData('../Downloads/randoms_DR9_CMASS_South.fits', npoints)
    print "Concat Now"
    DpRn = dataDDn + dataRRn
#    DpRs = dataDDs + dataRRs
    print "First hist"
    histDDnb = correlation.histBB(dataDDn)
    histDpRnb = correlation.histBB(DpRn)
    histRRnb = correlation.histBB(dataRRn)
    histDDna = correlation.histAA(dataDDn)
    histDpRna = correlation.histAA(DpRn)
    histRRna = correlation.histAA(dataRRn)
#    histDDs = correlation.histAA(dataDDs)
#    histDpRs = correlation.histAA(DpRs)
#    histRRs = correlation.histAA(dataRRs)

    histDRtop = correlation.histTopTri(dataDDn, dataRRn)
    histDRbot = correlation.histBotTri(dataDDn, dataRRn)

    corrHistb = correlationHistogram(histDDnb, histDpRnb, histRRnb)
    corrHista = correlationHistogram(histDDna, histDpRna, histRRna)
                                    
    c = r.TCanvas()
    outFileName = "Correlation FunctionB.pdf"
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

    outFileName = "Correlation FunctionA.pdf"
    c.Print(outFileName + "[")
    corrHista.Draw()
    c.Print(outFileName)
    histDDna.Draw()
    c.Print(outFileName)
    histRRna.Draw()
    c.Print(outFileName)
    histDpRna.Draw()
    c.Print(outFileName)
    c.Print(outFileName + "]")
    print corrHistb.GetBinContent(corrHistb.GetNbinsX()+1)
    print corrHista.GetBinContent(corrHista.GetNbinsX()+1)
    assert corrHista = corrHistb
