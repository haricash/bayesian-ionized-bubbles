# Functions I have written for calculating various cosmological quantities, etc.

import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import quad



# Parameters
box_size = 128
cell_size = 2
H_0 = 67.8
c = 3e+8
z_B = 6.998720204767237
omega_m = 0.308
omega_l = 0.692
units = 3000/0.678
h = 0.678
k_B = 1.38e-23

# Hubble Function
def H(r,z): return np.sqrt(omega_m*(1+z)**3 + omega_l)/units
def H_inv(z): return units/np.sqrt(omega_m*(1+z)**3 + omega_l)

############################
# Note : Need to make these 
# functions more usable
############################

### Coordinate conversions
def redshift_to_frequency(z):
    """
    Input : redshift
    Output : frequency in MHz
    """
    nu = 1420/(1+z) 
    return nu

# Converting box coordinates to redshift
def box_to_redshift(r,z_i=z_B):
    """
    Input cell location in grid in integers
    """
    r = cell_size*r + 1
    
    if type(r) == int :
        z = solve_ivp(H, t_span=[32,r], y0=[z_i], method='LSODA', rtol=1e-08,atol=1e-08)
        return z.y[-1][-1]

    else :
        list = []
        for i in r :
            z = solve_ivp(H, t_span=[32,i], y0=[z_i], method='LSODA', rtol=1e-08,atol=1e-08)
            list.append(z.y[-1][-1])

        return np.array(list)

# Converting redshift to distance
def redshift_to_distance(z_i=0,z_f=z_B):
    """
    Input: 
        z_i = Lower redshift limit
        z_f = Upper redshift limit
    Output:
        Distance in comoving units
    """
    r = quad(H_inv,z_i,z_f)[0]
    return r

# Converting box coordinates to angle
def redshift_to_angle(z, x=box_size):
    """
    Input : 
        Redshift of object z 
        Width of object x in cMpc (default box_size)
    Output :
        Angle in arcmins
    """
    theta = x/(h*redshift_to_distance(0,z))
    return theta * 180/np.pi * 60

# Converting angle to box coordinates
def angle_to_box(theta, z):
    """
        Input angle(radians) and redshift
    """
    x = (((2*units/((omega_m)**0.5))/(1-(1+z)**(-0.5)) * theta) - 1)/2
    return x

# Convert from flux density to Jansky
def flux_to_jy(flux, bandwidth=8.03e6):
    return 1e26 * flux / bandwidth

# Convert Jansky to temperature
def jy_to_k(flux,freq,size):
    """
        Converts from flux in Jy to temperature in K using Rayleigh Jeans approx.
    """
    return flux * c**2 / (2*k_B*(freq**2)*(size**2))

# Convert brightness temperature to Jansky
def k_to_jy(temp, size, freq):
    """
        Converts from temperature in K to flux in Jy
    """
    return 2*k_B*temp*freq**2*size**2/ c**2

# Converting from longitude/latitude to uv coordinates
def latlong2uvw(wavelength,hour_angle,declination,ref_hour_angle,ref_declination,longitude,latitude):
    """
    Tries to convert from latitude and longitude to uv coodinates
    Assumes that the w coordinate is suppressed because of small variations
    """

    # Redefining the parameters
    hour_angle = hour_angle + ref_hour_angle
    declination = declination + ref_declination
    
    # Defining the transformation matrix
    transformation = np.array([[np.sin(hour_angle), np.cos(hour_angle)],
                                [-np.sin(declination)*np.cos(hour_angle), np.sin(declination)*np.sin(hour_angle)]])
    coordinates = np.array([longitude,latitude])
    
    # Actual conversion from one set of coordinates to another
    u,v = 1/wavelength * np.matmul(transformation,coordinates)
    
    return u,v
################################################################################

# Average brightness temperature
def Tbar_b(z):
    return 22*((1+z)/7)**(0.5)

# For getting the brightness temperature map
def brightness_temperature_map(cell_array, Delta_HI_arr, unionized_HI_arr):
    """
    Converts neutral hydrogen maps to brightness temperature maps
    Input :
        cell_array : Array of grid cells in the box
        Delta_HI_arr : Neutral Hydrogen density field
        unionized_HI_arr : Unionized hydrogen field. Pass in 1 - qi_array
    Output : 
        The 21cm brightness map one would observe
    """
    return Tbar_b(box_to_redshift(cell_array)) * Delta_HI_arr * unionized_HI_arr

# Calculating the sky specific intensity
def sky_intensity(array, frequency):
    """
    Returns the sky specific intensity of the observed brightness
    temperature. The expression is given as 
    .. math ::
        I = 2 k_B \nu ^2 / c^2 \delta T_B
    """
    return 2 * k_B * frequency**2 * array / c**2

# For getting the gridded visibilities
def visibility(array, frequency, baseline_sampling_function, primary_beam_pattern=1):
    """
    Converts the input signal array into a gridded visibility
    Input :
        array : The sky intensity as an array
        frequency : The frequency at which the observation is being made
        baseline_sampling_function : The baseline sampling function of the interferometer
        primary_beam_pattern : The antenna's primary beam pattern
    Output :
        The gridded visibility at the given frequency 
    """
    return baseline_sampling_function * np.fft.fft2(primary_beam_pattern*sky_intensity(array))

# For obtaining noise map
def noise_map(T_sys, A_eff, del_nu_c, t_c):
    """
    Creates a 3D visibility noise map given the input parameters
    Input :
    T_sys = system temperature
    A_eff = effective collecting area
    t_c = correlator integrator time
    del_nu_c = frequency resolution of the observation
    """
    np.random.seed(42)

    rms_dev = np.sqrt(2/(del_nu_c * t_c)) * k_B * T_sys / A_eff
    dim = int(box_size/cell_size)
    return np.random.normal(0,rms_dev,size=(dim, dim, dim))

def cube_fft(data_cube):
    length = 64
    fft_slice = np.zeros((length, length, length), dtype=np.complex64)
    for i in range(length):
        fft_slice[:,:,i] = np.fft.fftshift(np.fft.fft2(data_cube[:,:,i]))

    # fft_slice = np.fft.fftshift(np.fft.fft2(data_cube))
    return fft_slice
    
# Radial profile
def radial_profile(data, center):
    """
        Returns the radial profile of the input array
    """
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    r = r.astype(np.int32)
    data = np.abs(data)
    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return np.abs(radialprofile)