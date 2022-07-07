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
        Width of object x (default box_size)
    Output :
        Angle in arcmins
    """
    theta = x/h * redshift_to_distance(0,z)
    return theta * 180/np.pi * 60

# Converting angle to box coordinates
def angle_to_box(theta, z):
    """
        Input angle(radians) and redshift
    """
    x = (((2*units/((omega_m)**0.5))/(1-(1+z)**(-0.5)) * theta) - 1)/2
    return x

# Convert Jansky to temperature
def jy_to_k(flux,freq,size):
    """
        Converts from flux to temperature using Rayleigh Jeans approx.
    """
    return c**2 / (2 * k_B * np.power(freq, 2) * np.power(size, 2)) * flux

# Converting from longitude/latitude to uv coordinates
def enu2uvw(wavelength,hour_angle,declination,ref_hour_angle,ref_declination,e,n):
    """
    Tries to convert from latitude and longitude to uv coodinates
    Assumes that the w coordinate is suppressed because of small variations
    """

    # Redefining the parameters
    hour_angle = (hour_angle + ref_hour_angle)*np.pi/12
    declination = (declination + ref_declination)*np.pi/180
    
    # Defining the transformation matrix
    transformation = np.array([[np.sin(hour_angle), np.cos(hour_angle)],
                                [np.cos(declination)*np.cos(hour_angle), np.cos(declination)*np.sin(hour_angle)]])
    coordinates = np.array([e,n])
    
    # Actual conversion from one set of coordinates to another
    u,v = 1/wavelength * np.matmul(transformation,coordinates)
    
    return u,v

# From latlong to ecef

def latlong2ecef(latitude,longitude):
    
    latitude = latitude*np.pi/180
    latitude = longitude*np.pi/180
    R = 6471

    X = R*np.cos(latitude)*np.sin(longitude)
    Y = R*np.cos(latitude)*np.cos(longitude)
    Z = R*np.sin(latitude)

    return X,Y,Z

# From ecef to enu
def ecef2enu(X,Y,Z,latitude,longitude,):
    transformation = np.array([[-np.sin(longitude), np.cos(longitude)],[-np.sin(latitude)*np.cos(longitude)]])