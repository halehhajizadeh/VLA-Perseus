# First index is Stokes
# Second index is frequency
# Third index is DEC
# Fourth index is RA
import sys
sys.path.append('.')
import os
import numpy as np
from astropy.io import fits

# Parameters (define them directly instead of importing)
nit = 5000
specific_dirs = '03:32:04.530001_+31.05.04.00000/'  # Example specific directory; update as needed

# Base path for data
base_path = "../data"  # Base directory for data
path = os.path.join(base_path, "concat", specific_dirs)

stokes_list = ['I', 'Q', 'U']

# Function to create an empty channel FITS file using astropy
def create_empty_channel(fitsname):
    flagged_channel = os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits')

    # Remove existing empty channel file if it exists
    syscommand = f'rm -rf {flagged_channel}'
    os.system(syscommand)

    # Open the FITS file, set the data to NaN, and save as a new file
    with fits.open(fitsname) as hdul:
        img_fits = hdul[0].data
        img_fits[:] = np.nan  # Set all data to NaN

        # Create an empty FITS file
        hdul.writeto(flagged_channel, overwrite=True)

    return flagged_channel

# Function to remove empty channels from the start of the file list
def remove_empty_channel_from_start(filelist):
    if not filelist:
        return []
    if "empty_channel.fits" not in filelist[0]:
        return filelist
    else:
        return remove_empty_channel_from_start(filelist[1:])

# Process for each Stokes parameter
for stokes in stokes_list:
    cubename = os.path.join(path, f'Images/img{nit}/Stokes{stokes}.fits')

    # Remove any existing cube file
    syscommand = f'rm -rf {cubename}'
    os.system(syscommand)

    # Read the list of FITS files for the current Stokes parameter
    stokes_file = os.path.join(path, f'Images/img{nit}/Stokes{stokes}.txt')
    with open(stokes_file, 'r') as f:
        file_list = f.read().splitlines()

    # Remove any leading empty channel files from the list
    file_list = remove_empty_channel_from_start(file_list)

    # Adding the first channel to the list and initializing the cube
    inputfile = file_list[0]

    # Assuming paths in the file are already correct, no need to modify them
    full_inputfile_path = inputfile

    if not os.path.exists(full_inputfile_path):
        raise FileNotFoundError(f"File {full_inputfile_path} does not exist")

    # Open the FITS file using astropy
    with fits.open(full_inputfile_path) as hdul:
        img = hdul[0].data  # Get the data for the first channel
        cube = np.copy(img)  # Copy it to initialize the cube

    # Create an empty channel FITS file
    create_empty_channel(full_inputfile_path)
    print('Empty channel is produced!')

    # Loop through the file list, appending data to the cube
    for filename in file_list:
        full_filename_path = filename

        if not os.path.exists(full_filename_path):
            print(f"Warning: File {full_filename_path} does not exist, skipping")
            continue

        with fits.open(full_filename_path) as hdul:
            imgCP = hdul[0].data
            if filename == os.path.join(path, f'Images/img{nit}/fits/empty_channel.fits'):
                # Replace NaN values with 1e30 to avoid issues
                imgCP[np.isnan(imgCP)] = 1e30
            img2cube = np.copy(imgCP)
            cube = np.append(cube, img2cube, axis=0)

    print('For loop completed!')

    # Save the completed cube to the output FITS file
    hdu = fits.PrimaryHDU(cube)
    hdu.writeto(cubename, overwrite=True)

    print(f'Making cube for Stokes {stokes} is done!')
