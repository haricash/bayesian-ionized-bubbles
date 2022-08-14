# Code for the filter(signal) to be used in the likelihood calculation

import numpy as np
# from skimage import morphology

box_size = 128 #hinv cMpc
cell_size = 2 #hinv cMpc
max_rad = box_size/2

bandwidth = 8.037 #MHz
freq_res = 0.125 #MHz
freq_ext = bandwidth/2

ang_ext = 73.4778/2 #arcmin
ang_res = 1.14809 #arcmin

def sphere_idx(shape, radius, position):
    """Generate an n-dimensional spherical mask."""
    assert len(position) == len(shape)
    n = len(shape)
    position = np.array(position).reshape((-1,) + (1,) * n)
    arr = np.linalg.norm(np.indices(shape) - position, axis=0)
    return arr <= radius


def signal(radius, theta_x, theta_y, del_nu, amp_del):
    """Generates the filter"""
	
    filter_instance = np.zeros((64,64,64))

    if (0 < radius <= max_rad) and (-ang_ext < theta_x <= ang_ext) and (-ang_ext < theta_y <= ang_ext) and (-freq_ext < del_nu <= freq_ext) and (amp_del > 0):
        
        # write functions for converting the natural units to coordinate units

        radius = radius/box_size *64
        theta_x = theta_x*32/ang_ext + 32
        theta_y = theta_y*32/ang_ext + 32
        del_nu = (del_nu/freq_ext + 1) * 32

        filter_instance = sphere_idx((64,64,64), radius, (theta_x,theta_y,del_nu))
        filter_instance = np.logical_not(filter_instance).astype(np.int32)
    	
    return filter_instance*amp_del
    