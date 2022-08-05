import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("/home/haricash/Sem 7/Project/code-scripts/bubbles/modules")
from functions import cube_fft, radial_profile

#Prepping visibility data for a spherical source
vis_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/spherical_bubble.npy")

# vis_data = np.fft.fft2(vis_data)
vis_data = cube_fft(vis_data)
vis_data = np.abs(vis_data)
# vis_data = np.fft.fftshift(vis_data)

noise_data = np.load("/home/haricash/Sem 7/Project/code-scripts/bubbles/datafiles/noise_cube.npy")
noise_data = np.abs(noise_data)

def freq_profile(radius, data):
    
    length = len(data[radius,radius,:])
    profile = np.zeros(length)
    
    for i in range(length):
        profile[i] = radial_profile(data[:, :, i], [32,32])[radius]

    return profile

y_vis = np.abs(freq_profile(1, vis_data))
y_noise = np.abs(freq_profile(1, noise_data))

x = (np.arange(64) - 32) * 4.015/32
plt.plot(x, y_vis, label="Visibility Data")
plt.plot(x, y_noise, label="Noise Data")

plt.grid()
plt.legend()
plt.xlabel(r"$\Delta \nu$ [MHz]")
plt.ylabel(r"$Amplitude |S(U = 46.786, \nu)|$ Jy")
# plt.xscale('log')
# plt.yscale('log')
plt.title("Variation in Visibility and Noise Amplitude wrt frequency")


plt.show()