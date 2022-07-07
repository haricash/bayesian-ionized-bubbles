# Code for creating the baseline maps for the given observation

import numpy as np
import matplotlib.pyplot as plt
from modules.conversions import enu2uvw

e = np.loadtxt("ska-enu.dat", usecols=0)
n = np.loadtxt("ska-enu.dat", usecols=1)
u = np.loadtxt("ska-enu.dat", usecols=2)

e_array = []
n_array = []
u_array = []

length = len(e)

for i in range(length):
    for j in range(length):
        e_array.append(e[i]-e[j])
        n_array.append(n[i]-n[j])
        u_array.append(u[i]-u[j])


e_array = np.array(e_array)
n_array = np.array(n_array)

# Creating a single instant uv map 
u,v = enu2uvw   (wavelength=1.680, 
                hour_angle=0,
                declination=0, 
                ref_declination=-30, 
                ref_hour_angle=0,
                e=e_array, 
                n=n_array)
np.save("uv-array.npy",(u,v))

plt.scatter(u,v,s=0.1)
plt.xlabel("u [dimensionless]")
plt.ylabel("v [dimensionless]")
plt.title(r"Baseline Distribution ($\nu$ = 177.5 MHz)")
# plt.grid()
plt.savefig("baseline-map.png", bbox_inches="tight")