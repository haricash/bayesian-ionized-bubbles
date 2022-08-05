from cProfile import label
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("/home/haricash/Sem 7/Project/code-scripts/bubbles/modules")
from functions import radial_profile

#Prepping Noise Data
noise_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/noise_data.npy")
noise_data = noise_data * 1e+26

center = [int(len(noise_data)/2), int(len(noise_data)/2)]

# noise_data = np.fft.fft2(noise_data)
# noise_data = np.fft.fftshift(noise_data)

#Prepping visibility data for a spherical source
vis_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/spherical_bubble.npy")[:,:,32]
vis_data = vis_data
vis_data = np.fft.fft2(vis_data)
vis_data = np.fft.fftshift(vis_data)

noise_rad = radial_profile(np.abs(noise_data), center)
vis_rad = radial_profile(np.abs(vis_data), center)

baseline = np.linspace(46.786, 2995.837, len(noise_rad))

plt.plot(baseline[:-1], noise_rad[:-1], label="Noise Profile")
plt.plot(baseline, vis_rad, label="Visibility Profile")
plt.yscale('log')
plt.xscale('log')
plt.xlabel(r"Baseline Length U")
plt.ylabel(r"Amplitude $|S(U,\nu = 177.5 MHz)|$ Jy")
plt.legend()
plt.title("Radial Profiles for Visibility and Noise")
# plt.grid()
plt.savefig("diagnostic_plots.png", bbox_inches="tight")