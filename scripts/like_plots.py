import sys
import numpy as np
import matplotlib.pyplot as plt

from modules.functions import cube_fft
from likelihood import log_likelihood

noise_data = np.load("datafiles/noise_cube.npy")
noise = np.std(noise_data)
noise = noise**2
# noise = np.power(noise, -2, dtype=np.float64)
# noise = np.ones((64,64,64))

visibility = np.load("datafiles/spherical_bubble.npy")
# visibility = np.asarray(visibility)
visibility = cube_fft(visibility)

def like_rad():
    rad_range = np.linspace(5,35,100)
    rad_dist = [log_likelihood(mu=(i,0,0,0,0.005632), visibility=visibility, noise=noise) for i in rad_range]
    return rad_range, rad_dist

def like_theta_x():
    theta_range = np.linspace(-20,20,100)
    theta_valx = [log_likelihood(mu=(20, i, 0, 0, 0.005632), visibility=visibility, noise=noise) for i in theta_range]
    return theta_range, theta_valx


def like_theta_y():
    theta_range = np.linspace(-20,20,100)
    theta_valy = [log_likelihood(mu=(20, 0, i, 0, 0.005632), visibility=visibility, noise=noise) for i in theta_range]
    return theta_range, theta_valy

def like_del_nu():
    nu_range = np.linspace(-2, 2, 100)
    nu_vals = [log_likelihood(mu=(20, 0, 0, i, 0.005632), visibility=visibility, noise=noise) for i in nu_range]
    return nu_range, nu_vals

def like_amp():
    amp_range = np.linspace(0,0.010,100)
    amp_vals = [log_likelihood(mu=(20, 0, 0, 0, i), visibility=visibility, noise=noise) for i in amp_range]
    return amp_range, amp_vals

def plotter(func):
    plt.plot(func[0], func[1])
    
    plt.xlabel(r"$A_{\delta T_b}$")
    plt.ylabel(r"log($\Lambda$)")
    plt.title(r"Conditional Likelihood of $A_{\delta T_b}$")#; True $R$ = 20 $h^{-1} cMpc$")
    plt.axvline(x = 0.005632, color='black', linestyle='--', alpha=0.5)
    plt.grid()
    plt.show()

plotter(like_amp())