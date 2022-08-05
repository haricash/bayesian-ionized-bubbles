import numpy as np
import matplotlib.pyplot as plt

from modules.functions import cube_fft

a = np.load("datafiles/spherical_bubble.npy")
a = cube_fft(a)

plt.plot(a[32,34,:])
plt.show()