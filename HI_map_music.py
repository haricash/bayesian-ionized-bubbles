# Code for the getting the cosmological data from SCRIPT
### Import all required modules

import numpy as np
import script

### Getting the data from the MUSIC snapshot

music_snapshot = '/home/haricash/Software/music/music_outputs/snap_029' # Obtaining a snapshot from z ~ 7
output_path = '/home/haricash/Sem 7/Project/code-scripts/output-files/denvel-fields' # Storing the output files
scaledist = 1e-3
default_simulation_data = script.default_simulation_data(music_snapshot,output_path,sigma_8=0.829,ns=0.961,
                                                        omega_b=0.0482, scaledist=scaledist)

ngrid = 64
matter_fields = script.matter_fields(default_simulation_data, ngrid, output_path, overwrite_files=False)

log10_M_min = 8.3
fcoll_arr = matter_fields.get_fcoll_for_Mmin(log10_M_min)

### Creating ionization fields and maps
ionization_map = script.ionization_map(matter_fields) # compute ionization field

zeta = 8 # effective ionization efficiency
qi_arr = ionization_map.get_qi(zeta*fcoll_arr) # ionized hydrogen fraction
qi_mean = np.mean(qi_arr * (1 + matter_fields.densitycontr_arr)) # Mean mass averaged ionized fraction

# print(qi_mean, np.max(qi_arr))

# Initialize power spectrum plans and set the k-bins
matter_fields.initialize_powspec()
k_edges, k_bins = matter_fields.set_k_edges(nbins=15,log_bins=True)
Delta_HI_arr = (1 - qi_arr) * (1 + matter_fields.densitycontr_arr) # HI density field
powspec_21cm, kount = ionization_map.get_binned_powspec(Delta_HI_arr, k_edges, units='mK') # HI power spectra in mK
mass_avg_ion_frac = qi_arr * (1 + matter_fields.densitycontr_arr)

np.save('density_contrast_array.npy', (1 + matter_fields.densitycontr_arr), allow_pickle=False) # Test data to check if power spectrum of HI and mass match
np.save('mass_avg_ion_frac.npy', mass_avg_ion_frac, allow_pickle=False) # Mass averaged ionized fraction
np.save('HI_output.npy',Delta_HI_arr, allow_pickle=False) # HI fraction in each bin
np.save('ionized_region.npy',qi_arr, allow_pickle=False) # Ionized fraction in each bin
np.save('21cm_pow_spec.npy',np.array([[powspec_21cm], [k_bins]]), allow_pickle=False) # 21 cm power spectrum

print("Task Complete!")
