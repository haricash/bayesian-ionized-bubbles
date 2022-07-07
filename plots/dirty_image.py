import sys
sys.path.insert(0, "/home/haricash/Sem 7/Project/code-scripts/bubbles/modules")

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from functions import sky_intensity, flux_to_jy, visibility

delta_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/lc_slice.npy")
# delta_data = delta_data[:,:,0]
baseline_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/gridded_uv.npy")
sky_intensity_map = sky_intensity(delta_data, 177.5e+6)
sky_intensity_map_jy = flux_to_jy(sky_intensity_map)

visibility_map = np.fft.fft2(sky_intensity_map_jy)
visibility_map = np.fft.fftshift(visibility_map)
# dirty_image = np.roll(np.roll(dirty_image, 32, axis=0), 32, axis=1)
# baseline_data = 1
sky_signal = baseline_data*visibility_map

dirty_image = np.fft.ifftshift(sky_signal)
dirty_image = np.fft.ifft2(sky_signal).real

dirty_image_jy = dirty_image

np.save("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/dirty_image.npy", dirty_image_jy)
np.save("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/sky_signal.npy", sky_signal)

# sys.exit(0)

# print("Dirty image max is", np.max(dirty_image_jy))
# print("Image max is", np.max(sky_intensity_map_jy))

# dirty_image = baseline_data

### Plotting stuff

figure_mosaic = """
AAB
AAC
"""
fig, axs = plt.subplot_mosaic(layout=figure_mosaic, figsize=(10,5),
                              constrained_layout=True
                             )



# Dirty Image
im1 = axs["A"].imshow(dirty_image_jy, interpolation='gaussian', origin='lower',
            vmin=np.min(dirty_image_jy), vmax=np.max(dirty_image_jy), extent=[0,73.47,0,73.47])
axs["A"].set_xlabel(r"$\theta_1$ [arcmin]")
axs["A"].set_ylabel(r"$\theta_2$ [arcmin]")
axs["A"].set_title("Dirty Image")

divider1 = make_axes_locatable(axs["A"])
cax1 = divider1.append_axes("right", size="5%", pad=0.05)
cb1 = fig.colorbar(im1, cax=cax1)
cb1.set_label(r"Jansky")
cb1.formatter.set_powerlimits((0,0))

# Sky intensity map
im2 = axs["B"].imshow(sky_intensity_map_jy, interpolation='gaussian', origin='lower',
            vmin=np.min(sky_intensity_map_jy), vmax=np.max(sky_intensity_map_jy), extent=[0,73.47,0,73.47])
axs["B"].set_xlabel(r"$\theta_1$ [arcmin]")
axs["B"].set_ylabel(r"$\theta_2$ [arcmin]")
axs["B"].set_title("Sky Intensity Map")

divider2 = make_axes_locatable(axs["B"])
cax2 = divider2.append_axes("right", size="5%", pad=0.05)
cb2 = fig.colorbar(im2, cax=cax2)
cb2.set_label(r"Jansky")
cb2.formatter.set_powerlimits((0,0))

# Baseline distribution function
im3 = axs["C"].imshow(baseline_data, origin='lower', vmin=0, vmax=1, extent=[-2995.837, 2995.837, -2995.837, 2995.837])
axs["C"].set_xlabel(r"u")
axs["C"].set_ylabel(r"v")
axs["C"].set_title("Baseline Distribution Function")


divider3 = make_axes_locatable(axs["C"])
cax3 = divider3.append_axes("right", size="5%", pad=0.05)
cb3 = fig.colorbar(im3, cax=cax3)
cb3.set_label(r"Boolean")
cb3.formatter.set_powerlimits((0,0))

# fig.suptitle(r"Observing at 177.5 MHz")
# fig.tight_layout()
# plt.savefig("dirty_image.png", bbox_inches="tight")
plt.show()