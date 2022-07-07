# Plots the mass weighted ionized fraction of the slice

import numpy as np
import matplotlib.pyplot as plt

mass_avg_ion_frac = np.load('datafiles/mass_avg_ion_frac.npy')
mass_avg_ion_frac = mass_avg_ion_frac.flatten().squeeze()
# print(np.max(mass_avg_ion_frac), np.mean(mass_avg_ion_frac))

range = np.arange(start=0,stop=4,step=0.05)

# Making the plot 
fig, ax1 = plt.subplots()
bin_nos,qi = np.histogram(mass_avg_ion_frac, bins=range) # The bin sizes for the power spectrum are set by the k_bins etc whatever

heights = bin_nos/np.sum(bin_nos)

ax1.bar(qi[1:],heights, align='edge', width=-0.05,alpha=0.5)

# ax1.set_facecolor('#E4E4E4')
ax1.set_xlabel("Value of ionized fraction")
ax1.set_ylabel("Probability Density (logscale)")
ax1.set_title("Probability Density Distribution \n of Mass Weighted Ionized Fraction (Mean = 0.46)")
ax1.set_yscale('log')
plt.savefig("mass_avg_ion_frac_hist.png", bbox_inches="tight")