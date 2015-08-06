#!/usr/bin/env python

import numpy as np
from astropy.io import fits
from astropy.table import Table
import ROOT as r
import common

print "Starting Now"

r.gROOT.SetBatch(1)
data = fits.getdata('data/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)

print "Opened First Table"

#data1 = fits.getdata('data/randoms_DR9_CMASS_North.fits', 1)
#t1 = Table(data1)

#print "Opened Second Table"

#h = r.TH1D("Data Redshift Weighted", "Data Redshift Weighted;Redshift;Counts", 100, 0.43, 0.7)
#h7 = r.TH1D("Random Redshift Weighted", "Random Redshift Weighted;Redshift;Counts", 100, 0.43, 0.7)
h2 = r.TH1D("Comoving Distance", "Random Dc;Mpc;Counts", 100, 
            common.comovingDistance(.43), 
            common.comovingDistance(.7))
h3 = r.TH1D("Luminosity Distance", "Random Dl;Mpc;Counts", 100,
            common.luminosityDistance(.43),
            common.luminosityDistance(.7))

print "Filling Data Histogram"

for row in t:
   ra = row['ra']
   dec = row['dec']
   z = row['z']
#   wcp = row['weight_cp']
 #  wfkp = row['weight_fkp']
  # wrf = row['weight_noz']
   #wsys = row['weight_sdc']
   #w = wfkp*wsys*(wrf + wcp + 1)
   h2.Fill(common.comovingDistance(z))
   h3.Fill(common.luminosityDistance(z))
#print "Filling Random Histogram"

#for row in t1:
 #  z1 = row['z']
  # w1 = row['weight']
  # h7.Fill(z1)

print "Drawing"

c = r.TCanvas()
h2.Draw()
c.Print("ComovingDistanceGalaxy.pdf")
h3.Draw()
c.Print("LuminosityDistanceGalaxy.pdf")
#h7.Draw()
#c.Print("Random Z Un-Weighted.pdf")

#for row in t:
 #  wnoz = row['weight_noz']
  # assert wnoz == 1.0
