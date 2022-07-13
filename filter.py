# Code for the filter(signal) to be used in the likelihood calculation

import numpy as np
# from skimage import morphology

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

    if (0 < radius <= 63) and (0 < theta_x <= 63) and (0 < theta_y <= 63) and (0 < del_nu <= 63) and (amp_del > 0):
        filter_instance = sphere_idx((64,64,64), radius, (theta_x,theta_y,del_nu))
        filter_instance = np.logical_not(filter_instance).astype(np.int32)
    	
    return filter_instance*amp_del


# An attempt at writing a class for the signal. Need to work on it later
# Do we even need this to be an object? I don't think so

# class Signal:
    
    # def __init__(self, radius, image):
        # self.radius = radius
        # self.image = image

    # def footprint(self):
        # return morphology.disk(self.radius)
    
    # def res(self):
        # return morphology.black_tophat(self.image, self.footprint())

    # def centre_location(self):
        ## minima_footprint = morphology.local_minima(self.image + self.res())
        # return morphology.local_minima(self.image + self.res(), footprint=self.footprint(), indices=True)
