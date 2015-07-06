import numpy as np
from astropy.io import fits
from astropy.table import Table
import ROOT as r

print "Starting Now"

r.gROOT.SetBatch(1)
data = fits.getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)

print "Opened First Table"

#data1 = fits.getdata('../Downloads/randoms_DR9_CMASS_North.fits', 1)
#t1 = Table(data1)

#print "Opened Second Table"

h = r.TH1D("Data Redshift Weighted", "Data Redshift Weighted;Redshift;Counts", 100, 0.43, 0.7)
#h7 = r.TH1D("Random Redshift Weighted", "Random Redshift Weighted;Redshift;Counts", 100, 0.43, 0.7)

print "Filling Data Histogram"

for row in t:
   ra = row['ra']
   dec = row['dec']
   z = row['z']
   wcp = row['weight_cp']
   wfkp = row['weight_fkp']
   wrf = row['weight_noz']
   wsys = row['weight_sdc']
   w = wfkp*wsys*(wrf + wcp + 1)
   h.Fill(z, w)
#print "Filling Random Histogram"

#for row in t1:
 #  z1 = row['z']
  # w1 = row['weight']
  # h7.Fill(z1)

print "Drawing"

c = r.TCanvas()
h.Draw()
c.Print("Data Z Weighted sdc.pdf")
#h7.Draw()
#c.Print("Random Z Un-Weighted.pdf")

for row in t:
   wnoz = row['weight_noz']
   assert wnoz == 1.0
