import sys
sys.path.append('.')
import numpy as np
import os

# Define parameters
nit = 5000  # Number of iterations (nit parameter)
thresh = '2e-4'  # Threshold for the FITS images
spw = [15, 16, 17, 0, 1, 2, 3, 4, 5, 6, 7, 8]  # Spectral windows (SPWs)
channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']  # Channels
stokes = ['I', 'Q', 'U']  # Stokes parameters

# Define the specific directory you're using for concatenation
specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # Update the directory as needed

# Define the base path for concatenation task
path = f"../data/concat/{specific_dirs}"

# Path to the FITS files
fits_path = os.path.join(path, f"Images/img{nit}/fits/")
file_list = [file for file in os.listdir(fits_path) if os.path.isfile(os.path.join(fits_path, file))]

# Create a complete list of file paths
file_list_total = [os.path.join(fits_path, file) for file in file_list]
print(f"Total files found: {len(file_list_total)}")

# Step 1: Build the list of images for each Stokes parameter
def build_image_list(stok):
    files_list = []
    for s in spw:
        for channel in channels:
            # Construct the expected file name
            file_name = os.path.join(fits_path, f"spw{s}-{channel}-2.5arcsec-nit{nit}-{thresh}-{stok}.image.smo.fits")
            # Append to the list (empty channel if file does not exist)
            if file_name in file_list_total:
                files_list.append(file_name)
            else:
                files_list.append(os.path.join(fits_path, "empty_channel.fits"))
    return files_list

# Step 2: Remove empty channels from the beginning of the list
def remove_initial_empty_channels(files_list):
    # Find the first non-empty channel in the list
    non_empty_start = 0
    for file_name in files_list:
        if "empty_channel.fits" not in file_name:
            break
        non_empty_start += 1
    # Return the updated list starting from the first non-empty channel
    return files_list[non_empty_start:], non_empty_start

# Step 3: Process and save the list for each Stokes parameter
def process_images(files_list, stok):
    # Save the list of files for the current Stokes parameter
    np.savetxt(os.path.join(path, f"Images/img{nit}/", f"Stokes{stok}.txt"), files_list, fmt='%s')
    print(f"File list for Stokes {stok} saved.")

# Main loop to process each Stokes parameter
for stok in stokes:
    # Step 1: Build the list of images for the current Stokes parameter
    files_list = build_image_list(stok)
    
    # Step 2: Remove the empty channels from the beginning of the cube
    non_empty_files_list, non_empty_start = remove_initial_empty_channels(files_list)
    
    # Step 3: Process and save the list for the current Stokes parameter
    process_images(non_empty_files_list, stok)
