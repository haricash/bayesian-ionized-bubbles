import numpy as np
import script
from reion_eff import quasar_zetafunc

music_snapshot = '/home/haricash/software/music/music_outputs/snap_029' # Obtaining a snapshot from z ~ 7
output_path = '/home/haricash/academic/coursework/Sem 7/Project/code-scripts/output-files/denvel-fields' # Storing the output files
scaledist = 1e-3
default_simulation_data = script.default_simulation_data(music_snapshot,output_path,sigma_8=0.829,ns=0.961,
                                                        omega_b=0.0482, scaledist=scaledist)

ngrid = 64
matter_fields = script.matter_fields(default_simulation_data, ngrid, output_path, overwrite_files=False)
ionization_map = script.ionization_map(matter_fields) 



log10Mmin = 8.3

zeta_fcoll_arr = matter_fields.get_zeta_fcoll(quasar_zetafunc, log10Mmin=log10Mmin)
qi_arr = ionization_map.get_qi(zeta_fcoll_arr)

Delta_HI_arr = (1 - qi_arr) * (1 + matter_fields.densitycontr_arr)

np.save('quasar_output.npy',Delta_HI_arr, allow_pickle=False)