import numpy as np
from astropy.io import fits
from astropy.table import Table
#import matplotlib.pyplot as plt
import ROOT as r
import hubble

#Current Speed of light in km/s
c = 3e8
#Current dimensionless scale factor
h = 0.72
#Current Hubble Constant in km/s/Mpc
H0 = 100*h
#Current Hubble Distance in Mpc
Dh = 3000/h

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
h2 = r.TH1D("Hubble Ratio", "H(z);Mpc;Counts per bin", 100, hubble.hubbleRatio(zlo), hubble.hubbleRatio(zhi))
h3 = r.TH1D("Comoving Distance", "Comoving Distance;Mpc;Counts per bin", 100, hubble.comovingDistance(zlo), hubble.comovingDistance(zhi) )
h4 = r.TH1D("Angular Distance", "Angular Distance;Redshift;Counts per bin", 100, hubble.angularDistance(zlo), hubble.angularDistance(zhi) )
h5 = r.TH1D("Luminosity Distance", "Luminosity Distance;Redshift;Counts per bin", 100, hubble.luminosityDistance(zlo), hubble.luminosityDistance(zhi))
h6 = r.TH1D("Comoving Angular Diameter Distance", "Comoving Angular Diameter Distance;Redshift;Counts per bin", 100, hubble.comovingAngularDiameterDistance(zlo), hubble.comovingAngularDiameterDistance(zhi))


for row in t:
   ra = row['ra']
   dec = row['dec']
   z = row['z']
   h.Fill(ra)
   h1.Fill(ra, dec)
   h2.Fill(hubble.hubbleRatio(z))
   h3.Fill(hubble.comovingDistance(z))
   h4.Fill(hubble.angularDistance(z))
   h5.Fill(hubble.luminosityDistance(z))
   h6.Fill(hubble.comovingAngularDiameterDistance(z))

c = r.TCanvas()
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
h6.Draw()
c.Print("DComoving Angular Diameter Distance")
h.Draw()
c.Print("DRight Ascension.pdf")
