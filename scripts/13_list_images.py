import sys
sys.path.append('.')
import numpy as np
import os

# Define parameters
nit = 5000
thresh = '2e-4'
spw = [9, 10, 11, 12, 13, 14, 15, 16, 17, 0, 1, 2, 3, 4, 5, 6, 7, 8]
channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']
stokes = ['I', 'Q', 'U']


# specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # Using the same directory as in the first script
# specific_dirs =  '03:36:00.000000_+30.30.00.00001/' 
# specific_dirs =  '03:34:30.000000_+31.59.59.99999/'
specific_dirs =  '03:25:30.000000_+29.29.59.99999/'
# specific_dirs =  '03:23:30.000001_+31.30.00.00000/'

# Define the path for concatenation task
path = f"../data/concat/{specific_dirs}"

# Get list of FITS files in the directory
fits_path = os.path.join(path, f"Images/img{nit}/fits/")
file_list = [file for file in os.listdir(fits_path) if os.path.isfile(os.path.join(fits_path, file))]

# Create a complete list of file paths
file_list_total = [os.path.join(fits_path, file) for file in file_list]
print(file_list_total)

# Loop over stokes, SPWs, and channels
for stok in stokes:
    files_list = []
    for s in spw:
        for channel in channels:
            # Build expected file name based on previous script's format
            file_name = os.path.join(fits_path, f"spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo.fits")
            
            # Check if file exists, otherwise append empty channel file
            if file_name in file_list_total:
                files_list.append(file_name)
            else:
                files_list.append(os.path.join(fits_path, "empty_channel.fits"))
    
    # Save the list of files for the current stokes parameter
    np.savetxt(os.path.join(fits_path, f"Stokes{stok}.txt"), files_list, fmt='%s')
