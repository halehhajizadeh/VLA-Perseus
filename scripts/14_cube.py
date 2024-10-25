import sys
sys.path.append('.')
import os
import numpy as np
from astropy.io import fits  # Keep astropy for handling FITS files

# Updated path with mosaic name (specific_dirs)
specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # As used in your previous scripts

# Update path to use mosaic name and concat directory
base_path = '../data/concat/'  # Assuming this is the base path as used before
path = os.path.join(base_path, specific_dirs)

# Modify niter as per request (change this to your desired value)
nit = 5000  # Example new niter value, adjust as per your needs

stokes_list = ['I', 'Q', 'U']

# Indices to replace with "empty_channel.fits" for each Stokes parameter
drop_indices = {
    'I': [41, 53, 80],  # Indices for Stokes I
    'Q': [41, 45, 49, 80],  # Indices for Stokes Q
    'U': [41, 48, 49, 80, 95]  # Indices for Stokes U
}

# Function to create an empty channel FITS file using astropy
def create_empty_channel(fitsname):
    flagged_channel = os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits')

    # Remove existing empty channel file if it exists
    if os.path.exists(flagged_channel):
        os.remove(flagged_channel)

    # Open the FITS file, set all data to NaN or 1e30, and create the empty channel
    with fits.open(fitsname) as hdul:
        img_fits = hdul[0].data
        img_fits[:] = np.nan  # Set all data to NaN
        hdul.writeto(flagged_channel, overwrite=True)

    return flagged_channel

# Process for each Stokes parameter
for stokes in stokes_list:
    cubename = os.path.join(path, f'Images/img{nit}/Stokes{stokes}.fits')

    # Remove any existing cube file
    if os.path.exists(cubename):
        os.remove(cubename)

    # Read the list of FITS files for the current Stokes parameter
    with open(os.path.join(path, f'Images/img{nit}/Stokes{stokes}.txt'), 'r') as f:
        file_list = f.read().splitlines()

    print(f'Processing Stokes {stokes}: Found {len(file_list)} files.')

    # Adding the first channel to the list and initializing the cube
    inputfile = file_list[0]
    with fits.open(inputfile) as hdulist:
        img = hdulist[0].data
        cube = np.copy(img[0, :, :, :])  # Copy it to initialize the cube

    # Create an empty channel FITS file
    empty_channel_file = create_empty_channel(inputfile)
    print('Empty channel is produced!')

    # Loop through the file list, appending data to the cube
    file_index = 0  # This is the actual index
    for filename in file_list:
        print(f"Processing file at index {file_index}: {filename}")

        # Check if the current index should be replaced with an empty channel
        if file_index in drop_indices.get(stokes, []):
            # Replace the file with empty_channel.fits
            print(f"Replacing index {file_index} with empty channel for Stokes {stokes}")
            filename = empty_channel_file  # Replace with the path to the empty channel

        # Load the file data
        try:
            with fits.open(filename) as hdulistCP:
                imgCP = hdulistCP[0].data
                if filename == empty_channel_file:
                    print(f"Using empty channel for index {file_index}")
                    # Replace NaN values with 1e30 to avoid issues
                    imgCP[np.isnan(imgCP)] = 1e30
                img2cube = np.copy(imgCP[0, :, :, :])
                cube = np.append(cube, img2cube, axis=0)
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

        file_index += 1  # Increment the file index

    print(f"For loop completed for Stokes {stokes}!")

    # Save the completed cube to the output FITS file
    try:
        hdulist[0].data = cube
        hdulist.writeto(cubename, overwrite=True)
        print(f"Cube saved for Stokes {stokes} at {cubename}")
    except Exception as e:
        print(f"Error saving cube for {stokes}: {e}")
