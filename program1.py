

import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt


data = fits.getdata('Downloads/galaxies_DR9_CMASS_North.fits', 1)
t = Table(data)
print(t[0]['ra'])

for row in t:
    print(row['ra'])
