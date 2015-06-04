#import numpy as np
from astropy.io import fits
from astropy.table import Table
#import matplotlib.pyplot as plt
import ROOT as r
import hubble

r.gROOT.SetBatch(1)
data = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)
print(t[0]['ra'])

h = r.TH1D("hist", "", 100, 105, 265)
h1 = r.TH2D("hist1", "", 100, 105, 265, 100, 0, 60)
h2 = r.TH1D("hist2", "", 100,hubble.hubbleRatio(0.4), hubble.hubbleRatio(0.75))

for row in t:
   ra = row['ra']
   dec = row['dec']
   z = row['z']
   h.Fill(ra)
   h1.Fill(ra, dec)
   h2.Fill(hubble.hubbleRatio(z))
   hubble.comovingDistance(z)

c = r.TCanvas()
h.Draw()
c.Print("output.pdf")
h1.Draw()
c.Print("output1.pdf")
h2.Draw()
c.Print("output2.pdf")

