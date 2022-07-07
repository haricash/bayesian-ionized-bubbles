# Converts from the WGS84 format of the SKA-Low-1 antenna positions to 
# required ENU format of coordinates

import pymap3d as pm
import numpy as np

longitude = np.loadtxt("datafiles/ska-1-low.dat", usecols=2, skiprows=1) 
latitude = np.loadtxt("datafiles/ska-1-low.dat", usecols=3, skiprows=1)

ref_longitude = longitude[0]
ref_latitude = latitude[0]

enu = pm.geodetic2enu(latitude[1:],longitude[1:],h=0,lat0=ref_latitude,lon0=ref_longitude,h0=0)
np.savetxt("ska-enu.dat", np.array(enu).transpose())

print(np.array(enu).shape)