import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
import ROOT as r

r.gROOT.SetBatch(1)
data = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)
print(t[0]['ra'])

h = r.TH1D("hist", "", 100, 100, 260)
for row in t:
   h.Fill(row['ra'])
c = r.TCanvas()
h.Draw()
c.Print("output.pdf")



