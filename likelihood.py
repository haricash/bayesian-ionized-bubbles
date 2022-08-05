# importing signal from sph_128

import numpy as np
from filter import signal
from modules.functions import cube_fft

grid_coord = None
visibility = None
noise = None

def log_likelihood(mu, grid_coord=grid_coord, visibility=visibility, noise=noise):
    """
    Calculates the log likelihood as defined in Ghara & Choudhury 2020
    
    Doesn't convert the input mu to an integer 

    Noise input should be in visibility space
    """
    # mu = np.array(mu).astype(int) #take care of this

    R, theta_x, theta_y, del_nu, amp_del = mu
    sig = signal(R, theta_x, theta_y, del_nu, amp_del)#.astype(np.float32)
    # S_f = np.fft.fft2(sig)
    # S_f = np.fft.fftshift(S_f)
    # noise = np.fft.fft2(noise)
    # noise = np.fft.fftshift(noise)
    S_f = cube_fft(sig)

    return np.sum((np.power(np.abs(visibility), 2) - np.power(np.abs(visibility - S_f), 2) )/np.power(np.abs(noise), 2))
