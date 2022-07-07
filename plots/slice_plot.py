# File not necessary - will delete this later
# But will continue using it as a reference of sorts ig
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Loading the data
ionized_grid = np.load('datafiles/ionized_region.npy')

# Scratch work
print(np.max(ionized_grid), np.min(ionized_grid), np.shape(ionized_grid))

# Plotting
fig,(ax1,ax2) = plt.subplots(1,2)

# For a x-y slice
im1 = ax1.imshow( ionized_grid[:,:,32], interpolation='gaussian', origin='lower',
            vmin=np.min(ionized_grid), vmax=np.max(ionized_grid), extent=[0,128,0,128])
ax1.set_xlabel("x [$cMpc h^{-1}$]")
ax1.set_ylabel("y [$cMpc h^{-1}$]")
ax1.set_title("x vs y")
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)
cb1 = fig.colorbar(im1, cax=cax1)
cb1.set_label("$Q_HII$")

# For a x-z slice
im2 = ax2.imshow( ionized_grid[:,32,:], interpolation='gaussian', origin='lower',
            vmin=np.min(ionized_grid), vmax=np.max(ionized_grid), extent=[0,128,0,128])
ax2.set_xlabel("x [$cMpc h^{-1}$]")
ax2.set_ylabel("y [$cMpc h^{-1}$]")
ax2.set_title("x vs y")
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="5%", pad=0.05)
cb2 = fig.colorbar(im1, cax=cax2)
cb2.set_label("$Q_HII$")

# For plotting finally
fig.suptitle("Ionized regions")
fig.tight_layout()
plt.show()