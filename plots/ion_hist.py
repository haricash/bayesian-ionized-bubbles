import numpy as np
import matplotlib.pyplot as plt

ionized_fraction = np.load('datafiles/ionized_region.npy')
ionized_fraction = ionized_fraction.flatten().squeeze()
# print(np.max(ionized_fraction), np.mean(ionized_fraction))
range = np.arange(start=0,stop=1.05,step=0.01)

# Making the plot 
fig, ax1 = plt.subplots()
bin_nos,qi = np.histogram(ionized_fraction, bins=range) # The bin sizes for the power spectrum are set by the k_bins etc whatever

heights = bin_nos/np.sum(bin_nos)

ax1.bar(qi[1:],heights, align='edge', width=-0.01,alpha=0.5, color='orange')

# print(qi,heights)

# ax1.set_facecolor('#E4E4E4')
ax1.set_xlabel("Value of ionized fraction")
ax1.set_ylabel("Probability Density (logscale)")
ax1.set_title("Probability Density Distribution of Ionized Fraction")
ax1.set_yscale('log')
ax1.set_xticks(np.arange(0,1.1,0.1))
plt.savefig("ionized_fraction_histogram", bbox_inches="tight")
