# Code for the filter(signal) to be used in the likelihood calculation

import numpy as np
# from skimage import morphology

def signal(radius, theta_x, theta_y, del_nu, amp_del):

    filter = np.zeros((64,64,64))

    if (0 <= radius < 64) and (0 <= theta_x < 64) and (0 <= theta_y < 64) and (0 <= del_nu < 64):

        for i in range(theta_x - radius, theta_x + radius):
            for j in range(theta_y - radius, theta_y + radius):
                for k in range(del_nu - radius, del_nu + radius):
                    if (i-theta_x)**2 + (j-theta_y)**2 + (k-del_nu)**2 <= radius**2 and (0 <= i < 64) and (0 <= j < 64) and (0 <= k <64) :
                        filter[i][j][k] = 1
    
        filter = amp_del * filter
    
    return filter


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