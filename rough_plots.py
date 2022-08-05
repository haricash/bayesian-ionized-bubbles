import numpy as np
import matplotlib.pyplot as plt
# from modules.functions import noise_map
from likelihood import log_likelihood
from modules.functions import cube_fft
# from sph_128 import signal

# sig = signal(12.5, 1, 36.7389, 0, 5)
# plt.imshow(sig[0,:,:])


# nu = 177.5
# sys_temp = 100 + 60*((nu/300)**(-2.55))
# t_obs = None

# noise = noise_map(T_sys=sys_temp, A_eff=962, del_nu_c=62.73e+3, t_c=10) # everything in W
# noise = (noise * 1e+26) #Jy

# grid_coord = np.mgrid[0:64:1, 0:64:1, 0:64:1].reshape(3,-1).T # defining the coord for the input vec
noise = np.load("datafiles/noise_cube.npy")
# noise = np.float32(noise*1e+26)

# Loading the data
visibility_data = np.load("datafiles/spherical_bubble.npy")
visibility_data = np.asarray(visibility_data)
visibility = cube_fft(visibility_data)
# visibility = np.fft.fft2(visibility_data)
# visibility = np.fft.fftshift(visibility)
# plt.imshow(visibility[:,:,32].real)


# print(visibility.shape)
# print(noise.shape)

# # This creates the noise map for the given telescope set up
# noise = noise_map(T_sys=sys_temp, A_eff=962, del_nu_c=62.73e+3, t_c=10)

rad_range = np.linspace(10,30,100)
theta_range = np.linspace(30,42,100)
nu_range = np.linspace(-0.2, 0.2, 100)
amp_range = np.linspace(0,50,100)

# rad_dist = [log_likelihood(mu=(i,36.7389,36.7389,0,30), visibility=visibility, noise=noise) for i in rad_range]
theta_valx = [log_likelihood(mu=(20,i, 36.7389, 0,30), visibility=visibility, noise=noise) for i in theta_range]
# theta_valy = [log_likelihood(mu=(20,36.7389, i, 0,30), visibility=visibility, noise=noise) for i in theta_range]
# nu_vals = [log_likelihood(mu=(20,36.7389, 36.7389, i,30), visibility=visibility, noise=noise) for i in nu_range]
# amp_vals = [log_likelihood(mu=(20,36.7389, 36.7389, 0, i), visibility=visibility, noise=noise) for i in amp_range]

# fig, axs = plt.subplots(5)

# axs[0] = 
# plt.plot(rad_range, rad_dist)
# axs[1] = 
plt.plot(theta_range, theta_valx)
# axs[2] = 
# plt.plot(theta_range, theta_valy)
# axs[3] = 
# plt.plot(nu_range, nu_vals)
# axs[4] = 
# plt.plot(amp_range, amp_vals)

plt.xlabel(r"R $(h^{-1} cMpc)$")
plt.ylabel(r"log($\Lambda$)")
plt.title(r"log[$\Lambda(R \| \theta_X, \theta_Y, \Delta \nu, A_{\delta Tb})]$ ; True R = $20 (h^{-1} cMpc)$")
plt.grid()
plt.show()
