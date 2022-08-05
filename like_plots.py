import numpy as np
import matplotlib.pyplot as plt

from modules.functions import cube_fft
from likelihood import log_likelihood

noise = np.load("datafiles/noise_cube.npy")

visibility = np.load("datafiles/spherical_bubble.npy")
visibility = np.asarray(visibility)
visibility = cube_fft(visibility)

def like_rad():
    rad_range = np.linspace(10,30,100)
    rad_dist = [log_likelihood(mu=(i,36.7389,36.7389,0,0.005632), visibility=visibility, noise=noise) for i in rad_range]
    return rad_range, rad_dist

def like_theta_x():
    theta_range = np.linspace(32,42,100)
    theta_valx = [log_likelihood(mu=(20, i, 36.7389, 0, 0.005632), visibility=visibility, noise=noise) for i in theta_range]
    return theta_range, theta_valx


def like_theta_y():
    theta_range = np.linspace(33,40,100)
    theta_valy = [log_likelihood(mu=(20, 36.7389, i, 0, 0.005632), visibility=visibility, noise=noise) for i in theta_range]
    return theta_range, theta_valy

def like_del_nu():
    nu_range = np.linspace(-0.2, 0.2, 100)
    nu_vals = [log_likelihood(mu=(20,36.7389, 36.7389, i, 0.005632), visibility=visibility, noise=noise) for i in nu_range]
    return nu_range, nu_vals

def like_amp():
    amp_range = np.linspace(0,0.010,100)
    amp_vals = [log_likelihood(mu=(20,36.7389, 36.7389, 0, i), visibility=visibility, noise=noise) for i in amp_range]
    return amp_range, amp_vals

def plotter(func):
    plt.plot(func[0], func[1])
    
    plt.xlabel(r"$A_{\delta Tb}$")
    plt.ylabel(r"log($\Lambda$)")
    plt.title(r"Conditional Likelihood of $A_{\delta Tb}$ ; True $A_{\delta Tb}$ = 5.632 mJy")
    plt.axvline(x = 0.005632, color='black', linestyle='--', alpha=0.5)
    plt.grid()
    plt.show()

plotter(like_amp())