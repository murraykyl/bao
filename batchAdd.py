#!/usr/bin/env python

import ROOT as r

r.gROOT.SetBatch(True)

tfile = r.TFile.Open("yeehaw.root")
histEp = tfile.Get("histEp")
histEpClone = histEp.Clone()

for i in range(1, 1+histEp.GetNbinsX()):
    histEpClone.SetBinContent(i, 
                              histEp.GetBinContent(i)*
                              histEp.GetBinCenter(i)**2)

c = r.TCanvas()
histEp.Draw()
c.Print("CorrelationRaw.pdf")
histEpClone.Draw()
c.Print("CorrelationFinal.pdf")
                             
