# Code in work :)
# Note that all the index values being passed are integers

import emcee
import numpy as np
import corner
from filter import signal
from modules.functions import noise_map
from multiprocessing import Pool
from likelihood import log_likelihood

nu = 177.5
sys_temp = 100 + 60*((nu/300)**(-2.55))
t_obs = None
grid_coord = np.mgrid[0:64:1, 0:64:1, 0:64:1].reshape(3,-1).T # defining the coord for the input vec

# Loading the data
visibility_data = np.load("datafiles/spherical_bubble.npy")
visibility_data = np.asarray(visibility_data)
visibility = np.fft.fft2(visibility_data)

# This creates the noise map for the given telescope set up
noise = noise_map(T_sys=sys_temp, A_eff=962, del_nu_c=62.73e+3, t_c=10)


# Defining probability functions

def model(mu, grid_loc):
    """
    Returns the value of the visibility
    for given values of parameters and index 

    The function automatically converts the 
    input variables from float to int
    """

    mu = np.array(mu).astype(int) # take care of this
    
    R, theta_x, theta_y, del_nu, amp_del = mu
    x1, x2, x3 = grid_loc
    fft_image = np.fft.fft2(signal(R, theta_x, theta_y, del_nu, amp_del))
    return fft_image[x1, x2, x3]

# def log_likelihood(mu, grid_coord=grid_coord, visibility=visibility, noise=noise):
    # """
    # Calculates the log likelihood as defined in Ghara & Choudhury 2020
    
    # Converts the input mu to an integer 
    # """
    # mu = np.array(mu).astype(int) #take care of this

    # R, theta_x, theta_y, del_nu, amp_del = mu

    # S_f = np.fft.fft2(signal(R, theta_x, theta_y, del_nu, amp_del)).flatten()

    # return np.sum((np.abs(visibility)**2 - np.abs(visibility - S_f)**2 )/noise)

def log_prior(mu):
    """
    Outputs uniform priors for each parameter 
    """
    R, theta_x, theta_y, del_nu, amp_del = mu
    if 0 < R < 64 and 0 <= theta_x <= 64 and 0 <= theta_y <= 64 and 0 <= del_nu <= 64 and -5 <= amp_del <= 5 :
        return 0.0
    else :
        return -np.inf

def log_prob(mu, grid_coord=grid_coord, visibility = visibility, noise=noise):
    """
    Defines the RHS of the Bayes Theorem (only numerator)
    
    Also converts the input mu from float to int
    """
    mu = np.array(mu).astype(int) # take care of this

    lp = log_prior(mu)
    if not np.isfinite(lp):
        return -np.inf
    else:
        return lp + log_likelihood(mu, grid_coord=grid_coord, visibility=visibility, noise=noise)

### Running the sampler

# Loading the data into the sampler
data = (grid_coord, visibility_data.reshape(-1), noise.reshape(-1)) # a data holder for our x,y,yerr
nwalkers = 32 # number of walkers
niter = 1000 # number of iterations for the MCMC to explore the probability space
initial = np.array([7, 30, 30, 30, 4]) # this is the initial guess for our theta
ndim = len(initial)
p0 = [np.array(initial) + 1e-3 * np.random.randn(ndim) for i in range(nwalkers)] # this is how we move from one 
# location to another - how to sample for each step


# Setting up a backend to store the data
filename = "output-data.h5"
backend = emcee.backends.HDFBackend(filename)
backend.reset(nwalkers, ndim)

# Defining the main part of the program for running
def main(p0,nwalkers,niter,ndim,log_prob,data):

    with Pool() as pool :

        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, pool=pool, backend=backend, args=data)

        print("Running burn-in...")
        p0, _, _ = sampler.run_mcmc(p0, 100, progress=True)
        sampler.reset()

        print("Running production...")
        pos, prob, state = sampler.run_mcmc(p0, niter, progress=True)
    
        print("Run Complete!")

    return sampler, pos, prob, state

# Running the program
sampler, pos, prob, state = main(p0,nwalkers,niter,ndim,log_prob,data)
