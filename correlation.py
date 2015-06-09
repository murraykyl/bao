from astropy.io import fits
from astropy.table import table
import numpy as np
import ROOT as r
import math
from scipy import integrate

#Set up Histogram
r.gROOT.setBATCH(1)

#Access the table we will use
data = getdata('../Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = table(data)

#Define Constants
c = 3e5     #km/s
h = 0.7     #dimensionless universe scale
H0 = 100*h  #km/s/Mpc
Dh = 3000/h #Mpc
omega = {"K0": 0,  #Curvature
         "M0": .3, #Matter
         "R0": 0,  #Radiation
         "L0": .7} #Cosmological Constant

#Define row arguments
for row in t:
   ra = row['ra']
   dec = row['dec']
   z1 = row['z']

#Define Primary Functions
def hubbleRatio(z):                                         #H(z)/H_0
    return sqrt( omega["K0"] * (1+z)**2 +
                 omega["M0"] * (1+z)**3 +
                 omega["R0"] * (1+z)**4 +
                 omega["L0"])

def distanceMeasure(z):                                     #Distance Measure
    return (integrate.quad(lambda:x, 1/hubbleRatio(x), 
                           0, z) / H0) * c

#Define New Variable and Convert to Cartesian Coordinates
r = distanceMeasure(z1)                #Comoving Distances
ra1 = math.degrees(ra)                 #Convert to Degrees
dec1 = math.degrees(dec)               #Convert to Degrees
x = r * math.cos(ra1) * math.cos(dec1) #X-Coordinate
y = r * math.sin(ra1) * math.cos(dec1) #Y-Coordinate
z = r * math.sin(dec1)                 #Z-Coordinate

#Define Distances between Galaxies
for i in range(len(t)):
    xd = x - x[i:]
    yd = y - y[i:]
    zd = z - z[i:]
dist = sqrt(xd**2 + yd**2 + zd**2)     #THIS IS OUR NEW VARIABLE FOR THE CORRELATION FUNCTION

#Create Correlation Function Method 1
def correlationDataData(i):
    for i in range(len(t)):
        return dist - dist[i:]

#Create Histogram for New Function
corr = r.TH1D("DD(re)", "Data-Data;Distance;Counts per Bin", 100, dataData(zlo), dataData(zhi))
for row in t:
    corr.Fill(dataData(dist))
c = r.Tcanvas()
corr/Draw()
c.Print("Data-Data.pdf")
