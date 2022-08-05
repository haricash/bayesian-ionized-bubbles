# This file generates the differential brightness temperature map of
# the sky and stores it as an image file

import sys
sys.path.insert(1, '/home/haricash/Sem 7/Project/code-scripts/bubbles/modules')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from functions import box_to_redshift, Tbar_b, brightness_temperature_map, Tbar_b

# Get the mass weighted hydrogen fraction
Delta_HI_arr = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/HI_output.npy")
qi_array = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/ionized_region.npy")
density_contrast_arr = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/density_contrast_array.npy")
# Getting the actual quantity

delta_Tb = brightness_temperature_map(np.arange(64), Delta_HI_arr, 1-qi_array)

np.save("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/delta_Tb.npy", delta_Tb)

# Scratch area

######
# average brightness temp
avg_Tb = Tbar_b(7.09) * (1-np.average(qi_array*density_contrast_arr))
print(avg_Tb)
######

# Saving a slice for our usage
# This if for activities like plotting, etc 
np.save("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/lc_slice.npy",delta_Tb[:,:,0])

# Plotting
fig,axs = plt.subplots()

# For a x-y slice
im1 = axs.imshow(delta_Tb[:,:,0], interpolation='gaussian', origin='lower',
            vmin=np.min(delta_Tb), vmax=np.max(delta_Tb), extent=[0,73.47,0,73.47])
axs.set_xlabel(r"$\theta_1$ [arcmin]")
axs.set_ylabel(r"$\theta_2$ [arcmin]")
axs.set_title("177.5 MHz")
divider1 = make_axes_locatable(axs)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)
cb1 = fig.colorbar(im1, cax=cax1)
cb1.set_label(r"$\delta T_b [mK]$")

# # For a x-y slice
# im2 = axs[0,1].imshow(delta_Tb[:,:,21], interpolation='gaussian', origin='lower',
#             vmin=np.min(delta_Tb), vmax=np.max(delta_Tb), extent=[0,74.4,0,74.4])
# axs[0,1].set_xlabel(r"$\theta_1$")
# axs[0,1].set_ylabel(r"$\theta_2$")
# axs[0,1].set_title("174.07 MHz")
# divider2 = make_axes_locatable(axs[0,1])
# cax2 = divider2.append_axes("right", size="5%", pad=0.05)
# cb2 = fig.colorbar(im2, cax=cax2)
# cb2.set_label(r"$\delta T_b$")

# # For a x-y slice
# im3 = axs[1,0].imshow(delta_Tb[:,:,42], interpolation='gaussian', origin='lower',
#             vmin=np.min(delta_Tb), vmax=np.max(delta_Tb), extent=[0,74.4,0,74.4])
# axs[1,0].set_xlabel(r"$\theta_1$")
# axs[1,0].set_ylabel(r"$\theta_2$")
# axs[1,0].set_title("176.70 MHz")
# divider3 = make_axes_locatable(axs[1,0])
# cax3 = divider3.append_axes("right", size="5%", pad=0.05)
# cb3 = fig.colorbar(im3, cax=cax3)
# cb3.set_label(r"$\delta T_b$")

# # For a x-y slice
# im4 = axs[1,1].imshow(delta_Tb[:,:,63], interpolation='gaussian', origin='lower',
#             vmin=np.min(delta_Tb), vmax=np.max(delta_Tb), extent=[0,74.4,0,74.4])
# axs[1,1].set_xlabel(r"$\theta_1$")
# axs[1,1].set_ylabel(r"$\theta_2$")
# axs[1,1].set_title("179.36 MHz")
# divider4 = make_axes_locatable(axs[1,1])
# cax4 = divider4.append_axes("right", size="5%", pad=0.05)
# cb4 = fig.colorbar(im4, cax=cax4)
# cb4.set_label(r"$\delta T_b$")

# For plotting finally
fig.suptitle(r"$\delta T_b$ map")
fig.tight_layout()
plt.savefig("delta_Tb.png", bbox_inches="tight")