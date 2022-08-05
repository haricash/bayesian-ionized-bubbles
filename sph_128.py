import numpy as np
from modules.functions import k_to_jy

box_size = 128 #hinv cMpc
cell_size = 1 #hinv cMpc
max_rad = box_size/2

bandwidth = 8.037 #MHz
freq_res = 0.1254/2 #MHz
freq_ext = bandwidth/2

ang_ext = 73.4778 #arcmin
ang_res = 1.14809/2 #arcmin

def sphere_idx(shape, radius, position):
    """Generate an n-dimensional spherical mask."""
    assert len(position) == len(shape)
    n = len(shape)
    position = np.array(position).reshape((-1,) + (1,) * n)
    arr = np.linalg.norm(np.indices(shape) - position, axis=0)
    return arr <= radius


def signal(radius, theta_x, theta_y, del_nu, amp_del):
    """Generates the filter"""
	
    filter_instance = np.zeros((128,128,128))

    if (0 < radius <= max_rad) and (0 < theta_x <= ang_ext) and (0 < theta_y <= ang_ext) and (-freq_ext < del_nu <= freq_ext) and (amp_del > 0):
        
        # write functions for converting the natural units to coordinate units
        # radius = radius * 100
        radius = radius*128/box_size
        theta_x = theta_x*128/ang_ext
        theta_y = theta_y*128/ang_ext
        del_nu = del_nu*128/freq_ext + 64

        filter_instance = sphere_idx((128,128,128), radius, (theta_x,theta_y,del_nu))
        filter_instance = np.logical_not(filter_instance).astype(np.int32)
    	
    return filter_instance*amp_del

# Spherical bubble
rad = 20 #hinv ckpc
# bandwidth = 8.03 #MHz
# freq_res = 0.1254 #MHz
# freq_ext = bandwidth/2

ang_ext = 73.4778 #arcmin
# ang_res = 1.14809 #arcmin

amp_del = 30 # mK
arcmin = 73.4778
radian = arcmin/60 * np.pi/180
freq = 177.5 * 1e+6

sig = signal(rad,ang_ext/2, ang_ext/2, 0, amp_del)
sig = k_to_jy(sig, radian, freq)
sig = sig * 1e+26
np.save("datafiles/sph_128.npy", sig) #Jy