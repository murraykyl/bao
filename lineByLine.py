import math
from scipy import integrate
import random
import numpy as np
from astropy.io import fits
from astropy.table import Table
import ROOT as r

c = 3e5     #km/s
h = 0.7     #dimensionless universe scale
H0 = 100*h  #km/s/Mpc
Dh = 3000/h #Mpc
omega = {"K0": 0,  #Curvature
         "M0": .3, #Matter
         "R0": 0,  #Radiation
         "L0": .7} #Cosmological Constant

def hubbleRatio(z):                             #H(z)/H_0
    return math.sqrt(omega["K0"] * (1+z)**2 +
                     omega["M0"] * (1+z)**3 +
                     omega["R0"] * (1+z)**4 +
                     omega["L0"])

def distanceMeasure(z):                         #Comoving Distance Measure
    return (integrate.quad(lambda m: 1/hubbleRatio(m), 
                           0, z)[0] / H0) * c

class ComovingDistance(object):
    """Lookup table for comoving distance"""
    
    def __init__(self, lo, hi, nPoints = 1000):
        self.lookup = [(z, distanceMeasure(z))
                       for z in np.arange(lo, hi, (hi-lo)/(nPoints-1))]
        self.lookup.append((hi, distanceMeasure(hi)))

    def __call__(self, z):
        lo = self.lookup[0][0]
        hi = self.lookup[-1][0]
        i = int((len(self.lookup)-1) * (z - lo) / (hi - lo))
        x0,y0 = self.lookup[i]
        x1,y1 = self.lookup[i+1]
        return y0 + (z - x0) * (y1 - y0) / (x1 - x0)

cd = ComovingDistance(0.43, 0.7)

def cartesian(row):                             #Convert to Cartesian Coordinates
    """Define New Variable and Convert to Cartesian Coordinates"""
    r = cd(row['z'])                            #Comoving Distances
    ra1 = math.pi*row['ra']/180                 #Convert to Radians
    dec1 = math.pi*row['dec']/180               #Convert to Radians
    x = r * math.cos(ra1) * math.cos(dec1)      #X-Coordinate
    y = r * math.sin(ra1) * math.cos(dec1)      #Y-Coordinate
    z = r * math.sin(dec1)                      #Z-Coordinate
    return x,y,z

def absoluteDistance(xd,yd,zd):                 #Define Distances between Galaxies
    return math.sqrt(xd**2 + yd**2 + zd**2)

def lineByLineAB(filename1, filename2, nStart, nEnd):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;Eta(d)", 100, 0, 5000)
    data1 = fits.getdata(filename1, 1)
    data2 = fits.getdata(filename2, 1)
    tab1 = Table(data1)
    tab2 = Table(data2)
    list1 = [cartesian(row) for row in tab1]
    list2 = [cartesian(row) for row in tab2]
    for i,(xi,yi,zi) in enumerate(list1):
        if i%1==0: print "i= ", i
        if nStart < i < nEnd:
            for xj,yj,zj in list2:
                d = absoluteDistance(xi-xj,yi-yj,zi-zj)
                hist.Fill(d)
        else:
            pass
    return hist
    
def lineByLineAA(filename, nStart, nEnd):
    hist = r.TH1D("%f"%random.random(), " ;Mpc;Eta(d)", 100, 0, 5000)
    data = fits.getdata(filename, 1)
    table = Table(data)
    list = [cartesian(row) for row in table]
    for i,(xi,yi,zi) in enumerate(list):
        if nStart < i < nEnd: 
            if i%1==0: print "i= ", i
            for xj,yj,zj in list[i+1:]:
                d = absoluteDistance(xi-xj, yi-yj, zi-zj)
                hist.Fill(d)
        else:
            pass
    return hist

if __name__=="__main__":

    filename1 = 
    filename2 = 
    if filename1 = filename2:
        lineHist = lineByLineAA(filename1, 0, 10)    
    else:
        doubleHist = lineByLineAB(filename1, filename2, 0, 10)
    
    c = r.TCanvas()
    outFileName = "LineByLine%s.pdf" %random.random()
    lineHist.Draw()
    doubleHist.Draw()
    c.Print(outFileName)




#    for row in t:
 #       ra1 = row['ra']
  #      dec1 = row['dec']
   #     z1 = row['z']
    #    wcp1 = row['weight_cp']
     #   wfkp1 = row['weight_fkp']
      #  wrf1 = row['weight_noz']
       # wsys1 = row['weight_sdc']
        #w1 = wfkp1*wsys1*(wrf1 + wcp1 + 1)
#        for row in t2:
 #           ra2 = row['ra']
  #          dec2 = row['dec']
   #         z2 = row['z']
    #        wcp2 = row['weight_cp']
     #       wfkp2 = row['weight_fkp']
      #      wrf2 = row['weight_noz']
       #     wsys2 = row['weight_sdc']
        #    w2 = wfkp2*wsys2*(wrf2 + wcp2 + 1)
            
       # w = w1*w2
            
