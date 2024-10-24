import sys
sys.path.append('.')
import numpy as np
import os

# Define parameters
nit = 5000  # Number of iterations
thresh = '2e-4'  # Threshold for the fits image
spw = [15, 16, 17, 0, 1, 2, 3, 4, 5, 6, 7, 8]  # Spectral windows
channels = ['00~07', '08~15', '16~23', '24~31', '32~39', '40~47', '48~55', '56~63']  # Channels within each SPW
stokes = ['I', 'Q', 'U']  # Stokes parameters

# Indices to replace with "empty_channel.fits" for each Stokes parameter after removing initial empty channels
drop_indices = {
    'I': [41, 53, 80],  # Indices for Stokes I to replace with "empty_channel.fits"
    'Q': [41, 45, 49, 80],  # Indices for Stokes Q to replace with "empty_channel.fits"
    'U': [41, 48, 49, 80, 95]  # Indices for Stokes U to replace with "empty_channel.fits"
}

# Define the specific directory you're using
specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # Adjust this directory as needed

# Define the path for concatenation task
path = f"../data/concat/{specific_dirs}"

# Path to the FITS files
fits_path = os.path.join(path, f"Images/img{nit}/fits/")
file_list = [file for file in os.listdir(fits_path) if os.path.isfile(os.path.join(fits_path, file))]

# Create a complete list of file paths
file_list_total = [os.path.join(fits_path, file) for file in file_list]
print(f"Total files found: {len(file_list_total)}")

# Step 1: Build the list of images for each Stokes parameter
def build_image_list():
    files_list = []
    for stok in stokes:
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
    # Remove all initial "empty_channel.fits" from the beginning of the list
    non_empty_start = 0
    for file_name in files_list:
        if "empty_channel.fits" not in file_name:
            break
        non_empty_start += 1
    # Return the updated list without the initial empty channels
    return files_list[non_empty_start:], non_empty_start

# Step 3: Replace images at specified indices after removing empty channels from the beginning
def apply_replacements(files_list, non_empty_start):
    # Loop through stokes and apply the replacements based on the adjusted indices
    for stok in stokes:
        final_list = []
        file_index = 0  # Keep track of the current index after removing initial empty channels
        for file in files_list:
            adjusted_index = file_index + non_empty_start  # Adjust the index after removing empty channels

            # Check if the current adjusted index is in the drop list for the current stokes
            if adjusted_index in drop_indices.get(stok, []):
                # Replace with empty channel if the index is in the drop list
                final_list.append(os.path.join(fits_path, "empty_channel.fits"))
                print(f"Replacing index {adjusted_index} for Stokes {stok} with empty channel.")
            else:
                final_list.append(file)

            file_index += 1  # Increment the file index

        # Save the list of files for the current Stokes parameter
        np.savetxt(os.path.join(path, f"Images/img{nit}/", f"Stokes{stok}.txt"), final_list, fmt='%s')
        print(f"File list for Stokes {stok} saved.")

# Step 1: Build the list of images
files_list = build_image_list()

# Step 2: Remove the empty channels from the beginning of the cube
non_empty_files_list, non_empty_start = remove_initial_empty_channels(files_list)

# Step 3: Apply the replacements at the specified indices
apply_replacements(non_empty_files_list, non_empty_start)
