import numpy as np
from filter import signal
from modules.functions import noise_map
from modules.functions import k_to_jy

# Spherical bubble
rad = 20 #hinv ckpc
# bandwidth = 8.03 #MHz
# freq_res = 0.1254 #MHz
# freq_ext = bandwidth/2

ang_ext = 73.4778 #arcmin
# ang_res = 1.14809 #arcmin

amp_del = 0.01276 # mK
arcmin = 73.4778
radian = arcmin/60 * np.pi/180
freq = 177.5 * 1e+6

sig = signal(rad,ang_ext/2, ang_ext/2, 0, amp_del)
sig = k_to_jy(sig, radian, freq)
sig = sig * 1e+26
np.save("datafiles/spherical_bubble.npy", sig) #Jy

nu = 177.5 #MHz
sys_temp = 100 + 60*((300/nu)**(2.55))
t_obs = None

noise = noise_map(T_sys=sys_temp, A_eff=962, del_nu_c=62.73e+3, t_c=10) # everything in W
noise = noise * 1e+26 #Jy
np.save("datafiles/noise_cube.npy", noise)

print(k_to_jy(amp_del, radian, freq)*1e+26, np.average(np.abs(noise)))