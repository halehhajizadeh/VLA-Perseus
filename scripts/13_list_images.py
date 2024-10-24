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

# Indices to replace with "empty_channel.fits" for each Stokes parameter

# Drop indices for case #32
# drop_indices = {
#     'I': [41, 53, 80],
#     'Q': [41, 45, 49, 80],
#     'U': [41, 48, 49, 80, 95]
# }

# Drop indices for case #36
drop_indices = {
    'I': [41, 48, 80],
    'Q': [41, 42, 48, 49],
    'U': [41, 48, 49]
}

# Drop indices for case #25
# drop_indices = {
#     'I': [41, 80],
#     'Q': [41, 48, 49, 79, 80],
#     'U': [41, 48, 49, 79, 80]
# }

# Define the specific directory you're using
specific_dirs = '03:36:00.000000_+30.30.00.00001/'
# other possible directories (commented for future use)
# specific_dirs = '03:32:04.530001_+31.05.04.00000/'
# specific_dirs = '03:34:30.000000_+31.59.59.99999/'
# specific_dirs = '03:25:30.000000_+29.29.59.99999/'
# specific_dirs = '03:23:30.000001_+31.30.00.00000/'

# Define the path for concatenation task
path = f"../data/concat/{specific_dirs}"

# Get list of FITS files in the directory
fits_path = os.path.join(path, f"Images/img{nit}/fits/")
file_list = [file for file in os.listdir(fits_path) if os.path.isfile(os.path.join(fits_path, file))]

# Create a complete list of file paths
file_list_total = [os.path.join(fits_path, file) for file in file_list]
print(f"Total files found: {len(file_list_total)}")

# Loop over stokes, SPWs, and channels
for stok in stokes:
    files_list = []
    file_index = 0  # Keep track of the current index across all files
    for s in spw:
        for channel in channels:
            # Build expected file name based on previous script's format
            file_name = os.path.join(fits_path, f"spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo.fits")
            
            # Check if the current file index is in the drop list for the current stokes
            if file_index in drop_indices.get(stok, []):
                # Replace with empty channel if the index is in the drop list
                files_list.append(os.path.join(fits_path, "empty_channel.fits"))
                print(f"Replacing index {file_index} for Stokes {stok} with empty channel.")
            elif file_name in file_list_total:
                files_list.append(file_name)
            else:
                files_list.append(os.path.join(fits_path, "empty_channel.fits"))
            
            file_index += 1  # Increment the file index
    
    # Save the list of files for the current Stokes parameter
    np.savetxt(os.path.join(path, f"Images/img{nit}/Stokes{stok}.txt"), files_list, fmt='%s')

    print(f"File list for Stokes {stok} saved with the appropriate empty channel replacements.")
