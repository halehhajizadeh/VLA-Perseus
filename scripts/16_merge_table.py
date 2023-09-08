import sys
sys.path.append('.')
from configs import path, thresh, nit
import sys
import numpy as np


# Bad frequency array needs to be verified!
# bad_freq=[1.33488986e+09,1.367053824000e+09,1.495142528000e+09,1.63113075e+09,1.679270016000e+09,1.68717376e+09,1.69517990e+09,1.751319808000e+09,1.759325440000e+09,1.879408512000e+09,1.887414016000e+09,1.93536435e+09,1.98340122e+09]

I_pro_file=str(sys.argv[1])
Q_pro_file=str(sys.argv[2])
U_pro_file=str(sys.argv[3])

def setup_columns(pro_file, noise_value, lines_to_skip=5):
    with open (pro_file, 'r') as file:
        lines = file.read().splitlines()[lines_to_skip:]
        lines = [ 
           [l.strip() for l in line.split()]
           for line in lines
        ]
        lines = np.array(lines).transpose()
        
        freq = np.double(lines[0])
        print(f"freq shape: {freq.shape}")
        flux = np.double(lines[1])
        print(f"flux shape: {flux.shape}")
        flag = np.double(lines[2])
        print(f"flag shape: {flag.shape}")
        noise = np.copy(freq) * 0.0 + noise_value
    return(freq, flux, flag, noise)



freq_I, flux_I, flag_I, noise_I = setup_columns(I_pro_file, 9*1e-5, lines_to_skip=5)
freq_Q, flux_Q, flag_Q, noise_Q = setup_columns(Q_pro_file, 9*1e-5, lines_to_skip=5)
freq_U, flux_U, flag_U, noise_U = setup_columns(U_pro_file, 9*1e-5, lines_to_skip=5)


for i in range(len(freq_I)):
   if (np.isnan(flux_I[i])):
     flag_I[i]=3
   if (np.isnan(flux_Q[i])):
     flag_Q[i]=3
   if (np.isnan(flux_U[i])):
     flag_U[i]=3



with open(path+"./Images/img"+str(nit)+"/RMsyn/final_results1"+".dat", "w") as f:
    print(len(flag_I))
    for i in range(len(flag_I)):
        if ((flag_I[i]<1) and (flag_Q[i]<1) and (flag_U[i]<1)):
            if ((freq_I[i]==freq_Q[i]) and (freq_I[i]==freq_U[i])):
                print(
                   "%15.8e  %15.8e  %15.8e  %15.8e  %15.8e  %15.8e  %15.8e  "
                   % (freq_I[i],flux_I[i],flux_Q[i],flux_U[i],noise_I[i],noise_Q[i],noise_U[i]),
                   file=f
                   )