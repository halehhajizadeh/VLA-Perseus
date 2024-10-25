import sys
sys.path.append('.')
import numpy as np
import os

# Define parameters
nit = 5000
thresh = '2e-4'
spw = [15, 16, 17, 0, 1, 2, 3, 4, 5, 6, 7, 8]
channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']
stokes = ['I', 'Q', 'U']

# Define the specific directory you're using for concatenation
# specific_dirs = '03:32:04.530001_+31.05.04.00000/'
specific_dirs = '03:36:00.000000_+30.30.00.00001/'
# specific_dirs = '03:25:30.000000_+29.29.59.99999/'
# specific_dirs = '03:23:30.000001_+31.30.00.00000/'



path = f"../data/concat/{specific_dirs}"
fits_path = os.path.join(path, f"Images/img{nit}/fits/")
file_list_total = [os.path.join(fits_path, file) for file in os.listdir(fits_path) if os.path.isfile(os.path.join(fits_path, file))]

# Step 1: Build the list of images for each Stokes parameter
def build_image_list(stok):
    files_list = []
    for s in spw:
        for channel in channels:
            file_name = os.path.join(fits_path, f"spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo.fits")
            # Append to the list (empty channel if file does not exist)
            if file_name in file_list_total:
                files_list.append(file_name)
            else:
                files_list.append(os.path.join(fits_path, "empty_channel.fits"))
    return files_list

# Step 2: Remove empty channels from the beginning of the list
def remove_initial_empty_channels(files_list):
    non_empty_start = 0
    for file_name in files_list:
        if "empty_channel.fits" not in file_name:
            break
        non_empty_start += 1
    return files_list[non_empty_start:]

# Main loop to process each Stokes parameter
for stok in stokes:
    files_list = build_image_list(stok)
    non_empty_files_list = remove_initial_empty_channels(files_list)
    np.savetxt(os.path.join(path, f"Images/img{nit}/", f"Stokes{stok}.txt"), non_empty_files_list, fmt='%s')
    print(f"File list for Stokes {stok} saved with {len(non_empty_files_list)} entries.")
