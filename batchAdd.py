#!/usr/bin/env python

import ROOT as r
import common

r.gROOT.SetBatch(True)

tfile = r.TFile.Open("totalDD.root")
histDD = tfile.Get("DDhist")

tfile2 = r.TFile.Open("totalRR.root")
histRR = tfile2.Get("RRhist")

tfile3 = r.TFile.Open("totalDR.root")
histDR = tfile3.Get("DRhist")

for h in [histDD, histDR, histRR]: h.Scale(1./h.Integral())
histEp = common.correlationHistogram(histDD, histDR, histRR)    
histEpClone = histEp.Clone()
histDDRR = histEp.Clone()
histDDRR.Reset()
histDDRR.Add(histDD, 1)
histDDRR.Divide(histRR)
histDDRRClone = histDDRR.Clone()

for i in range(1, 1+histEp.GetNbinsX()):
    histEpClone.SetBinContent(i, 
                              histEp.GetBinContent(i)*
                              histEp.GetBinCenter(i)**2)
    histDDRRClone.SetBinContent(i,
                                (histDDRR.GetBinContent(i)-1)*
                                histDDRR.GetBinCenter(i)**2)

tfile6 = r.TFile.Open("CorrelationFunction.root", "recreate")
histDD.Write()
histDR.Write()
histRR.Write()
histEp.Write()
histEpClone.Write()
histDDRRClone.Write()
tfile6.Close()

c = r.TCanvas()
histDD.Draw()
c.Print("DDRaw.pdf")
histRR.Draw()
c.Print("RRRaw.pdf")
histDR.Draw()
c.Print("DRRaw.pdf")
histEp.Draw()
c.Print("CorrelationRaw.pdf")
histEpClone.Draw()
c.Print("CorrelationFinal.pdf")
histDDRRClone.Draw()
c.Print("DDRRminus.pdf")
