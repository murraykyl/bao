import numpy as np
from astropy.io import fits
from astropy.table import Table
#import matplotlib.pyplot as plt
import ROOT as r
import hubble

r.gROOT.SetBatch(1)
data = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)

ra1 = t['ra']
dec1 = t['dec']
z1 = t['z']
ralo = min(ra1) - 1
rahi = max(ra1) + 1
declo = min(dec1) - 1
dechi = max(dec1) + 1
zlo = min(z1) - 0.01
zhi = max(z1) + 0.01

h = r.TH1D("Right Ascension", "Right Ascension;RA;Counts per bin", 100, ralo, rahi)
h1 = r.TH2D("Sky", "CMASS Sky Sample;RA;Dec", 100, ralo, rahi, 100, declo, dechi)
h2 = r.TH1D("Hubble Ratio", "H(z);Redshift;Counts per bin", 100, hubble.hubbleRatio(zlo), hubble.hubbleRatio(zhi))
h3 = r.TH1D("Comoving Distance", "Comoving Distance;Redshift;Counts per bin", 100, hubble.comovingDistance(zlo), hubble.comovingDistance(zhi) )
h4 = r.TH1D("Angular Distance", "Angular Distance;Redshift;Counts per bin", 100, hubble2.angularDistance(zlo), hubble2.angularDistance(zhi) )
h5 = r.TH1D("Luminosity Distance", "Luminosity Distance;Redshift;Counts per bin", 100, hubble2.luminosityDistance(zlo), hubble2.luminosityDistance(zhi))

for row in t:
   ra = row['ra']
   dec = row['dec']
   z = row['z']
   h.Fill(ra)
   h1.Fill(ra, dec)
   h2.Fill(hubble.hubbleRatio(z))
   h3.Fill(hubble.comovingDistance(z))
   h4.Fill(hubble2.angularDistance(z))
   h5.Fill(hubble2.luminosityDistance(z))

c = r.TCanvas()
h.Draw()
c.Print("DRight Ascension.pdf")
h1.Draw()
c.Print("DRA and Dec.pdf")
h2.Draw()
c.Print("DH(z).pdf")
h3.Draw()
c.Print("DComoving Distance.pdf")
h4.Draw()
c.Print("DAngular Distance.pdf")
h5.Draw()
c.Print("DLuminosity Distance.pdf")
