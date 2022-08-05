# Generates noise maps for the SKA-1-Low
import sys
sys.path.insert(1, '/home/haricash/Sem 7/Project/code-scripts/bubbles/modules')
# sys.path.insert(2, '/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles')

import numpy as np
from functions import noise_map
from conversions import jy_to_k
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


nu = 177.5
sys_temp = 100 + 60*((nu/300)**(-2.55)) # nu input is in MHz
t_obs = None

baseline_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/baseline_hist.npy")
noise_map_grid = noise_map(T_sys=sys_temp, A_eff=962, del_nu_c=126.3e+3, t_c=10)
baseline_corrected_noise = noise_map_grid[:,:,32]/np.sqrt(baseline_data)
baseline_corrected_noise[np.isinf(baseline_corrected_noise)] = 0

image_noise = baseline_corrected_noise
image_noise = np.fft.ifftshift(image_noise)
image_noise = np.fft.ifft2(image_noise).real

np.save("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/noise_data.npy", image_noise)

# Converting units
image_noise = np.power(10, 26, dtype="double") * image_noise *10**3 #(mJy)
# image_noise = jy_to_k(image_noise, freq=177.5 * 10**6, size=(74/60)*(180/np.pi))

# Plotting
fig,axs = plt.subplots(1)

# For a x-y slice
im1 = axs.imshow(image_noise, origin='lower',
            vmin=np.min(image_noise), vmax=np.max(image_noise), extent=[0,74.4,0,74.4])
axs.set_xlabel(r"$\theta_1$ [arcmin]")
axs.set_ylabel(r"$\theta_2$ [arcmin]")
axs.set_title("Noise at 177.5 MHz")
divider1 = make_axes_locatable(axs)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)
cb1 = fig.colorbar(im1, cax=cax1)
cb1.set_label(r"$mJy$")

fig.suptitle(r"Noise Map")
fig.tight_layout()
# plt.savefig("noise_map.png", bbox_inches="tight")
plt.show()