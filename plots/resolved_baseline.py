# This generates the baseline that will have the resolution 
# to pick up the signal we have simulated 

import numpy as np
import matplotlib.pyplot as plt

# Converts the baseline u-v array into one that has
# been snipped according to the required resolution
# and gridded accordingly to what is required for
# the problem

data = np.load("datafiles/uv-array.npy").transpose()
sqrt2 = np.sqrt(2)

def norm(u,v): return np.sqrt(np.power(u,2) + np.power(v,2))

norm_array = norm(data[:,0], data[:,1])
# print(norm_array.shape)

new_data = data[norm(data[:,0], data[:,1]) < 2995.837]
new_data = new_data[np.abs(new_data[:,0]) < 2995.837/sqrt2]
new_data = new_data[np.abs(new_data[:,1]) < 2995.837/sqrt2]

hist, x_edges, y_edges = np.histogram2d(new_data[:,0], new_data[:,1], bins=64)
hist = hist.T

gridded_uv = hist > 0

np.save("datafiles/gridded_uv.npy", gridded_uv)
np.save("datafiles/baseline_hist.npy", hist)

# DO THIS PART - LABEL THE AXES PLEASEEE
# fig, axs = np.subplots(gridded_uv)

plt.imshow(gridded_uv)
plt.colorbar()
# plt.scatter(new_data[:,0], new_data[:,1], s=0.1)
plt.savefig("resolved_baseline.png", bbox_inches="tight")
