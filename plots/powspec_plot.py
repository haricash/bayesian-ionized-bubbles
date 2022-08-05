# Plots the power spectrum of the slice

import numpy as np
import matplotlib.pyplot as plt

powspec_dat = np.load('datafiles/21cm_pow_spec.npy').squeeze(axis=1)

# print(powspec_dat.shape)

fig, ax1 = plt.subplots(1,1)
fig.suptitle("HI Power Spectrum")
ax1.plot(powspec_dat[1,:], powspec_dat[0,:] * (powspec_dat[1,:]**3)/(2 * np.pi**2))
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel("k bin scale   [$h c^{-1}Mpc^{-1}$]")
ax1.set_ylabel("$\Delta^2_{HI}(k) \ [mK^2]$")
ax1.set_title("$\Delta_{HI}^2(k)$ vs k")


plt.savefig("pow_spec.png", bbox_inches="tight")